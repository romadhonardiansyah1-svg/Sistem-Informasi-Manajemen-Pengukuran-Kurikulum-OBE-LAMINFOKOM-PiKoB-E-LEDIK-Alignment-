"""
CRUD RPS (Rencana Pembelajaran Semester).
Halaman 42-45 Buku Panduan APTIKOM.
"""

from flask import request

import state
from models.rps import RPS, RPSMinggu
from utils.response import success, created, not_found, error
from utils.pagination import get_pagination_params, apply_pagination
from services.lock_guard import assert_periode_unlocked


def list_rps():
    """GET /api/rps"""
    page, page_size = get_pagination_params()
    mk_id = request.args.get("mk_id", type=int)
    periode_id = request.args.get("periode_id", type=int)

    query = state.db.query(RPS)
    if mk_id:
        query = query.filter_by(mk_id=mk_id)
    if periode_id:
        query = query.filter_by(periode_id=periode_id)

    items, total = apply_pagination(query, page, page_size)
    return success(data=[i.to_dict() for i in items])


def get_rps(record_id):
    """GET /api/rps/<id>"""
    rps = state.db.query(RPS).get(record_id)
    if rps is None:
        return not_found()

    minggu_list = (
        state.db.query(RPSMinggu)
        .filter_by(rps_id=record_id)
        .order_by(RPSMinggu.minggu_ke)
        .all()
    )

    data = rps.to_dict()
    data["minggu"] = [m.to_dict() for m in minggu_list]
    return success(data=data)


def create_rps():
    """POST /api/rps"""
    data = request.get_json(silent=True)

    try:
        assert_periode_unlocked(data.get("periode_id"))
    except ValueError as e:
        return error(str(e), status=423)

    rps = RPS(
        mk_id=data["mk_id"],
        periode_id=data["periode_id"],
        kode_dokumen=data.get("kode_dokumen"),
        deskripsi_singkat=data.get("deskripsi_singkat"),
        pustaka_utama=data.get("pustaka_utama"),
        pustaka_pendukung=data.get("pustaka_pendukung"),
        dosen_pengampu=data.get("dosen_pengampu"),
        dosen_koordinator=data.get("dosen_koordinator"),
        tanggal_penyusunan=data.get("tanggal_penyusunan"),
    )
    state.db.add(rps)
    state.db.commit()
    return created(data=rps.to_dict())


def update_rps_minggu(record_id):
    """PUT /api/rps/<id>/minggu"""
    rps = state.db.query(RPS).get(record_id)
    if rps is None:
        return not_found()

    try:
        assert_periode_unlocked(rps.periode_id)
    except ValueError as e:
        return error(str(e), status=423)

    data = request.get_json(silent=True)
    minggu_data = data.get("minggu", [])

    state.db.query(RPSMinggu).filter_by(rps_id=record_id).delete()

    for m in minggu_data:
        minggu = RPSMinggu(
            rps_id=record_id,
            minggu_ke=m["minggu_ke"],
            sub_cpmk_id=m.get("sub_cpmk_id"),
            bentuk_pembelajaran=m.get("bentuk_pembelajaran"),
            metode_luring=m.get("metode_luring"),
            metode_daring=m.get("metode_daring"),
            materi=m.get("materi"),
            bobot_penilaian_persen=m.get("bobot_penilaian_persen", 0),
            indikator=m.get("indikator"),
            kriteria_teknik=m.get("kriteria_teknik"),
        )
        state.db.add(minggu)

    state.db.commit()
    return success(message="Data minggu diperbarui")


ROUTE_DEFINITIONS = [
    ("GET", "/api/rps", list_rps, "view_kurikulum"),
    ("GET", "/api/rps/<int:record_id>", get_rps, "view_kurikulum"),
    ("POST", "/api/rps", create_rps, "manage_rps"),
    ("PUT", "/api/rps/<int:record_id>/minggu", update_rps_minggu, "manage_rps"),
]
