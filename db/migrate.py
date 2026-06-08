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
]


def create_all():
    """Membuat seluruh tabel yang terdefinisi di models, lalu menambal kolom baru."""
    _import_all_models()
    Base.metadata.create_all(bind=state.engine)
    ensure_columns()


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


def drop_all():
    """Menghapus seluruh tabel. Hanya untuk development/testing."""
    _import_all_models()
    Base.metadata.drop_all(bind=state.engine)


def reset_db():
    """Drop lalu create ulang semua tabel."""
    drop_all()
    create_all()


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
