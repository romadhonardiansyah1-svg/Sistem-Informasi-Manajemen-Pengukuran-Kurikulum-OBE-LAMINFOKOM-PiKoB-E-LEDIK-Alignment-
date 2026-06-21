"""
Unit test sinkronisasi CPL-MK dari relasi CPL-BK x BK-MK.
Mengunci perbaikan bug indeks kolom (dulu memakai row[0]=id sehingga
menghasilkan pasangan salah dan merusak mapping_cpl_mk).
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _setup_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["DATABASE_URI"] = "sqlite:///" + path

    import importlib
    import config
    importlib.reload(config)
    import state
    from db.connection import init_db
    from db import migrate
    init_db()
    migrate.create_all()
    return path


def test_sync_cpl_mk_correct_pairs():
    path = _setup_db()
    try:
        import state
        from models.mapping import mapping_cpl_bk, mapping_bk_mk, mapping_cpl_mk
        from services.sync_service import sync_cpl_mk_from_relations

        # CPL1 -> BK10 ; CPL2 -> BK20
        state.db.execute(mapping_cpl_bk.insert().values(cpl_id=1, bk_id=10))
        state.db.execute(mapping_cpl_bk.insert().values(cpl_id=2, bk_id=20))
        # BK10 -> MK100, MK101 ; BK20 -> MK200
        state.db.execute(mapping_bk_mk.insert().values(bk_id=10, mk_id=100))
        state.db.execute(mapping_bk_mk.insert().values(bk_id=10, mk_id=101))
        state.db.execute(mapping_bk_mk.insert().values(bk_id=20, mk_id=200))
        state.db.commit()

        res = sync_cpl_mk_from_relations()

        rows = state.db.execute(mapping_cpl_mk.select()).fetchall()
        pairs = set((r.cpl_id, r.mk_id) for r in rows)
        expected = {(1, 100), (1, 101), (2, 200)}
        assert pairs == expected, "Pasangan CPL-MK salah: {}".format(pairs)
        assert res["total"] == 3
        print("test_sync_cpl_mk_correct_pairs: OK")
    finally:
        try:
            from db.connection import close_db
            close_db()
        except Exception:
            pass
        os.remove(path)


if __name__ == "__main__":
    test_sync_cpl_mk_correct_pairs()
    print("\nSemua test sync PASSED.")
