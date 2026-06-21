"""
Schema creation dan migration.
Membuat semua tabel berdasarkan model definitions.
"""

from sqlalchemy import text, inspect

import state
from models.base import Base


# Kolom baru yang ditambahkan setelah skema awal dibuat.
# create_all() hanya membuat TABEL yang belum ada, bukan KOLOM baru pada tabel
# yang sudah ada (mis. di Supabase produksi). ensure_columns() menambal hal ini.
_NEW_COLUMNS = [
    ("log_peninjauan", "jenis", "VARCHAR(40) DEFAULT 'peninjauan_kurikulum'"),
    ("log_peninjauan", "periode_id", "INTEGER"),
    ("log_peninjauan", "lokasi", "VARCHAR(200)"),
    ("dokumen_bukti", "storage_key", "VARCHAR(500) DEFAULT ''"),
    ("dokumen_bukti", "storage_backend", "VARCHAR(20) DEFAULT 'local'"),
    ("mahasiswa", "user_id", "INTEGER"),
    ("cpl_prodi", "referensi", "TEXT"),
    ("cpl_sn_dikti", "referensi", "TEXT"),
    ("bahan_kajian", "referensi", "TEXT"),
    ("rps", "bobot_teori_sks", "INTEGER DEFAULT 0"),
    ("rps", "bobot_praktikum_sks", "INTEGER DEFAULT 0"),
    ("rps", "media_software", "TEXT"),
    ("rps", "media_hardware", "TEXT"),
    ("rps", "mk_prasyarat", "TEXT"),
    # BUG-1: kolom yang ADA di model tapi belum terdaftar -> error di DB lama.
    ("profil_lulusan", "referensi", "TEXT"),
    ("profil_lulusan", "kategori", "VARCHAR(50)"),
    ("mata_kuliah", "jenis", "VARCHAR(20) DEFAULT 'wajib'"),
    ("mata_kuliah", "is_capstone", "BOOLEAN DEFAULT FALSE"),
    ("mata_kuliah", "prasyarat", "TEXT"),
    ("mata_kuliah", "deskripsi_singkat", "TEXT"),
    # MODUL 1: kolom referensi 3 sumber yang melekat di tiap data master.
    ("profil_lulusan", "ref_buku", "TEXT"),
    ("profil_lulusan", "ref_spreadsheet", "TEXT"),
    ("profil_lulusan", "ref_pikobe", "TEXT"),
    ("cpl_prodi", "ref_buku", "TEXT"),
    ("cpl_prodi", "ref_spreadsheet", "TEXT"),
    ("cpl_prodi", "ref_pikobe", "TEXT"),
    ("bahan_kajian", "ref_buku", "TEXT"),
    ("bahan_kajian", "ref_spreadsheet", "TEXT"),
    ("bahan_kajian", "ref_pikobe", "TEXT"),
    ("mata_kuliah", "referensi", "TEXT"),
    ("mata_kuliah", "ref_buku", "TEXT"),
    ("mata_kuliah", "ref_spreadsheet", "TEXT"),
    ("mata_kuliah", "ref_pikobe", "TEXT"),
    ("cpmk", "referensi", "TEXT"),
    ("cpmk", "ref_buku", "TEXT"),
    ("cpmk", "ref_spreadsheet", "TEXT"),
    ("cpmk", "ref_pikobe", "TEXT"),
]

# Migrasi nilai: salin kolom `referensi` lama -> `ref_buku` bila ref_buku kosong.
# (table, kolom_lama, kolom_baru) -- idempotent, hanya mengisi yang NULL.
_BACKFILL_COLUMNS = [
    ("profil_lulusan", "referensi", "ref_buku"),
    ("cpl_prodi", "referensi", "ref_buku"),
    ("bahan_kajian", "referensi", "ref_buku"),
]


def create_all():
    """Membuat seluruh tabel yang terdefinisi di models, lalu menambal kolom baru."""
    _import_all_models()
    Base.metadata.create_all(bind=state.engine)
    ensure_columns()
    backfill_columns()


def ensure_columns():
    """
    Menambahkan kolom baru pada tabel yang sudah ada (idempotent, lintas dialek).
    Memeriksa kolom yang sudah ada via inspector, lalu hanya menambahkan yang hilang.
    Aman dijalankan berulang pada SQLite (dev) maupun PostgreSQL/Supabase (prod).
    """
    if getattr(state, "engine", None) is None:
        return

    inspector = inspect(state.engine)
    existing_tables = set(inspector.get_table_names())

    for table, column, ddl in _NEW_COLUMNS:
        if table not in existing_tables:
            continue
        cols = {c["name"] for c in inspector.get_columns(table)}
        if column in cols:
            continue
        stmt = "ALTER TABLE {t} ADD COLUMN {c} {d}".format(t=table, c=column, d=ddl)
        try:
            with state.engine.begin() as conn:
                conn.execute(text(stmt))
            print("ensure_columns: added {}.{}".format(table, column))
        except Exception as e:
            print("ensure_columns skip {}.{}: {}".format(table, column, e))


def backfill_columns():
    """
    Menyalin nilai kolom lama `referensi` ke `ref_buku` bila `ref_buku` masih NULL.
    Idempotent dan aman dijalankan berulang. Hanya berjalan jika kedua kolom ada.
    """
    if getattr(state, "engine", None) is None:
        return

    inspector = inspect(state.engine)
    existing_tables = set(inspector.get_table_names())

    for table, src, dst in _BACKFILL_COLUMNS:
        if table not in existing_tables:
            continue
        cols = {c["name"] for c in inspector.get_columns(table)}
        if src not in cols or dst not in cols:
            continue
        stmt = (
            "UPDATE {t} SET {dst} = {src} "
            "WHERE {dst} IS NULL AND {src} IS NOT NULL".format(t=table, src=src, dst=dst)
        )
        try:
            with state.engine.begin() as conn:
                conn.execute(text(stmt))
        except Exception as e:
            print("backfill_columns skip {}.{}->{}: {}".format(table, src, dst, e))


def drop_all():
    """Menghapus seluruh tabel. Hanya untuk development/testing."""
    _import_all_models()
    Base.metadata.drop_all(bind=state.engine)


def reset_db():
    """Drop lalu create ulang semua tabel."""
    drop_all()
    create_all()


def clear_all_data():
    """
    Menghapus SEMUA baris dari setiap tabel (DML DELETE, TANPA DDL) dalam urutan
    aman-FK (tabel anak dulu). Dipakai untuk RE-SEED PAKSA tanpa drop tabel,
    sehingga aman di Supabase connection pooler (drop/create DDL bisa memutus SSL).
    Setelah ini, seed_all() akan mengisi ulang dari nol karena ProgramStudi kosong.
    """
    _import_all_models()
    if getattr(state, "engine", None) is None:
        return
    existing = set(inspect(state.engine).get_table_names())
    with state.engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            if table.name in existing:
                conn.execute(table.delete())
    print("clear_all_data: semua baris dihapus (siap re-seed).")


def _import_all_models():
    """
    Import semua module model agar SQLAlchemy
    mengetahui seluruh tabel yang perlu dibuat.
    """
    import models.institution
    import models.period
    import models.user
    import models.profil_lulusan
    import models.cpl
    import models.bahan_kajian
    import models.mata_kuliah
    import models.cpmk
    import models.sub_cpmk
    import models.mapping
    import models.penilaian
    import models.nilai
    import models.rps
    import models.log_peninjauan
    import models.master_dropdown
