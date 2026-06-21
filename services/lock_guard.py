"""
Guard untuk memastikan periode kurikulum tidak terkunci sebelum melakukan
operasi tulis (create/update/delete) pada master data.

Panggil assert_periode_unlocked(periode_id) di handler sebelum menulis.
Raise ValueError atau kembalikan error 423 jika periode terkunci.
"""

import state
from models.period import PeriodeKurikulum


def assert_periode_unlocked(periode_id):
    """
    Memeriksa apakah periode terkunci.
    Raise ValueError jika terkunci (HTTP 423 Locked).
    Jika periode_id None (belum terkait), lewati saja.
    """
    if not periode_id:
        return

    periode = state.db.query(PeriodeKurikulum).get(periode_id)
    if periode and getattr(periode, "locked", False):
        raise ValueError("Periode '{}' sudah terkunci. Buka kunci terlebih dahulu untuk mengubah data.".format(
            periode.nama or str(periode_id)
        ))


def is_periode_locked(periode_id):
    """Cek apakah periode terkunci (return bool)."""
    if not periode_id:
        return False
    periode = state.db.query(PeriodeKurikulum).get(periode_id)
    if periode is None:
        return False
    return bool(getattr(periode, "locked", False))


def assert_unlocked_by_mk(mk_id):
    """Guard periode lewat MK (resolve MataKuliah.periode_id)."""
    if not mk_id:
        return
    from models.mata_kuliah import MataKuliah
    mk = state.db.query(MataKuliah).get(mk_id)
    if mk is not None:
        assert_periode_unlocked(mk.periode_id)


def assert_unlocked_by_cpl(cpl_id):
    """Guard periode lewat CPL Prodi."""
    if not cpl_id:
        return
    from models.cpl import CPLProdi
    cpl = state.db.query(CPLProdi).get(cpl_id)
    if cpl is not None:
        assert_periode_unlocked(cpl.periode_id)


def assert_unlocked_by_bk(bk_id):
    """Guard periode lewat Bahan Kajian."""
    if not bk_id:
        return
    from models.bahan_kajian import BahanKajian
    bk = state.db.query(BahanKajian).get(bk_id)
    if bk is not None:
        assert_periode_unlocked(bk.periode_id)


def assert_unlocked_by_cpmk(cpmk_id):
    """Guard periode lewat CPMK (resolve via CPL induk)."""
    if not cpmk_id:
        return
    from models.cpmk import CPMK
    cpmk = state.db.query(CPMK).get(cpmk_id)
    if cpmk is not None:
        assert_unlocked_by_cpl(cpmk.cpl_id)
