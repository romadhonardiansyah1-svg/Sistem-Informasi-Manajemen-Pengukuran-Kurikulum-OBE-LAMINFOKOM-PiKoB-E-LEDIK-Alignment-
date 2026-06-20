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
