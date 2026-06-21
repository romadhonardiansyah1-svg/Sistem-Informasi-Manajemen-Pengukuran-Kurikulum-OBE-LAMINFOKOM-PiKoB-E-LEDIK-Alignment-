"""
Route laporan dan visualisasi CPL.
"""

from flask import request

import state
from services.report_service import (
    get_cpl_report_mahasiswa,
    get_cpl_report_agregat,
)
from utils.response import success, error


def report_cpl_mahasiswa():
    """GET /api/report/cpl/mahasiswa (staf/DPA: pilih mahasiswa_id)"""
    mahasiswa_id = request.args.get("mahasiswa_id", type=int)
    result = get_cpl_report_mahasiswa(mahasiswa_id)
    return success(data=result)


def report_cpl_saya():
    """
    GET /api/report/cpl/saya
    Laporan CPL milik mahasiswa yang sedang login (self-scoped).
    mahasiswa_id diturunkan dari akun, bukan dari query param,
    sehingga mahasiswa hanya bisa melihat capaiannya sendiri.
    """
    from models.user import Mahasiswa

    user = state.current_user
    mhs = state.db.query(Mahasiswa).filter_by(user_id=user.id).first()
    if mhs is None:
        return error("Akun ini belum tertaut ke data mahasiswa.", status=404)

    result = get_cpl_report_mahasiswa(mhs.id)
    result["mahasiswa"] = {
        "id": mhs.id,
        "nim": mhs.nim,
        "nama": mhs.nama,
        "angkatan": mhs.angkatan,
    }
    return success(data=result)


def report_cpl_agregat():
    """GET /api/report/cpl/agregat"""
    angkatan = request.args.get("angkatan", type=int)
    periode_id = request.args.get("periode_id", type=int)
    result = get_cpl_report_agregat(angkatan, periode_id)
    return success(data=result)


def list_mahasiswa():
    """GET /api/mahasiswa -- daftar mahasiswa untuk pemilih laporan/nilai."""
    from models.user import Mahasiswa

    angkatan = request.args.get("angkatan", type=int)
    query = state.db.query(Mahasiswa)
    if angkatan:
        query = query.filter_by(angkatan=angkatan)
    items = query.order_by(Mahasiswa.nim).all()
    return success(data=[
        {"id": m.id, "nim": m.nim, "nama": m.nama, "angkatan": m.angkatan}
        for m in items
    ])


ROUTE_DEFINITIONS = [
    ("GET", "/api/report/cpl/saya", report_cpl_saya, "view_report_self"),
    ("GET", "/api/report/cpl/mahasiswa", report_cpl_mahasiswa, "view_report"),
    ("GET", "/api/report/cpl/agregat", report_cpl_agregat, "view_report"),
    ("GET", "/api/mahasiswa", list_mahasiswa, "view_kurikulum"),
]
