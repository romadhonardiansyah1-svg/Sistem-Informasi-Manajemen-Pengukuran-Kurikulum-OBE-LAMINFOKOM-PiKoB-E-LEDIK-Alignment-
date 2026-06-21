"""
Unit test migrasi kolom (BUG-1 + MODUL 1).
Mensimulasikan DB lama yang belum punya kolom baru, lalu memverifikasi
ensure_columns() menambal kolom dan backfill_columns() menyalin referensi -> ref_buku.
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine, text, inspect

import state
from db import migrate


def _setup_old_db():
    """Buat sqlite dengan skema 'lama' (tanpa kolom baru) dan satu baris data."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    engine = create_engine("sqlite:///" + path)
    with engine.begin() as conn:
        # Skema lama profil_lulusan: hanya punya kolom dasar + referensi lama.
        conn.execute(text(
            "CREATE TABLE profil_lulusan ("
            "id INTEGER PRIMARY KEY, periode_id INTEGER, kode VARCHAR(10), "
            "deskripsi TEXT, referensi TEXT)"
        ))
        conn.execute(text(
            "INSERT INTO profil_lulusan (id, periode_id, kode, deskripsi, referensi) "
            "VALUES (1, 1, 'PL01', 'desk', 'Tabel 1 hal 15')"
        ))
        # Skema lama cpl_prodi & bahan_kajian untuk backfill.
        conn.execute(text(
            "CREATE TABLE cpl_prodi ("
            "id INTEGER PRIMARY KEY, periode_id INTEGER, kode VARCHAR(10), "
            "deskripsi TEXT, referensi TEXT)"
        ))
        conn.execute(text(
            "INSERT INTO cpl_prodi (id, periode_id, kode, deskripsi, referensi) "
            "VALUES (1, 1, 'CPL01', 'desk', 'Tabel 2 hal 17')"
        ))
        conn.execute(text(
            "CREATE TABLE mata_kuliah ("
            "id INTEGER PRIMARY KEY, periode_id INTEGER, kode VARCHAR(10), "
            "nama VARCHAR(200), sks INTEGER, semester INTEGER)"
        ))
    return engine, path


def test_ensure_columns_adds_missing():
    """Kolom baru (BUG-1 + MODUL 1) harus ditambahkan ke tabel lama."""
    engine, path = _setup_old_db()
    old_engine = getattr(state, "engine", None)
    state.engine = engine
    try:
        migrate.ensure_columns()
        insp = inspect(engine)

        pl_cols = {c["name"] for c in insp.get_columns("profil_lulusan")}
        for col in ("kategori", "ref_buku", "ref_spreadsheet", "ref_pikobe"):
            assert col in pl_cols, "profil_lulusan kurang kolom " + col

        mk_cols = {c["name"] for c in insp.get_columns("mata_kuliah")}
        for col in ("jenis", "is_capstone", "prasyarat", "deskripsi_singkat",
                    "ref_buku", "ref_spreadsheet", "ref_pikobe"):
            assert col in mk_cols, "mata_kuliah kurang kolom " + col
        print("test_ensure_columns_adds_missing: OK")
    finally:
        state.engine = old_engine
        engine.dispose()
        os.remove(path)


def test_backfill_referensi_to_ref_buku():
    """Nilai referensi lama harus tersalin ke ref_buku saat backfill."""
    engine, path = _setup_old_db()
    old_engine = getattr(state, "engine", None)
    state.engine = engine
    try:
        migrate.ensure_columns()
        migrate.backfill_columns()
        with engine.connect() as conn:
            pl = conn.execute(text(
                "SELECT referensi, ref_buku FROM profil_lulusan WHERE id=1"
            )).fetchone()
            assert pl[1] == "Tabel 1 hal 15", "ref_buku PL tidak ter-backfill"
            cpl = conn.execute(text(
                "SELECT ref_buku FROM cpl_prodi WHERE id=1"
            )).fetchone()
            assert cpl[0] == "Tabel 2 hal 17", "ref_buku CPL tidak ter-backfill"
        print("test_backfill_referensi_to_ref_buku: OK")
    finally:
        state.engine = old_engine
        engine.dispose()
        os.remove(path)


def test_ensure_columns_idempotent():
    """Menjalankan ensure_columns dua kali tidak boleh error."""
    engine, path = _setup_old_db()
    old_engine = getattr(state, "engine", None)
    state.engine = engine
    try:
        migrate.ensure_columns()
        migrate.ensure_columns()  # kedua kali: semua kolom sudah ada
        print("test_ensure_columns_idempotent: OK")
    finally:
        state.engine = old_engine
        engine.dispose()
        os.remove(path)


if __name__ == "__main__":
    test_ensure_columns_adds_missing()
    test_backfill_referensi_to_ref_buku()
    test_ensure_columns_idempotent()
    print("\nSemua test migrasi PASSED.")
