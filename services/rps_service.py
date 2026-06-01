"""
Logika bisnis RPS.
"""

import state
from models.rps import RPS, RPSMinggu


def get_rps_full(mk_id, periode_id):
    """Mengambil RPS lengkap dengan detail mingguan."""
    rps = (
        state.db.query(RPS)
        .filter_by(mk_id=mk_id, periode_id=periode_id)
        .first()
    )
    if rps is None:
        return None

    minggu_list = (
        state.db.query(RPSMinggu)
        .filter_by(rps_id=rps.id)
        .order_by(RPSMinggu.minggu_ke)
        .all()
    )

    data = rps.to_dict()
    data["minggu"] = [m.to_dict() for m in minggu_list]
    return data


def validate_rps_completeness(rps_id):
    """
    Memeriksa kelengkapan RPS.
    Return: list field yang belum diisi.
    """
    rps = state.db.query(RPS).get(rps_id)
    if rps is None:
        return ["RPS tidak ditemukan"]

    missing = []
    required_header = ("deskripsi_singkat", "pustaka_utama", "dosen_pengampu")
    for field in required_header:
        value = getattr(rps, field)
        if not value:
            missing.append(field)

    minggu_count = (
        state.db.query(RPSMinggu)
        .filter_by(rps_id=rps_id)
        .count()
    )

    if minggu_count < 16:
        missing.append("Jumlah minggu kurang dari 16")

    return missing
