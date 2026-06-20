"""
CRUD Bahan Kajian (BK).
Tabel 4 Buku Panduan APTIKOM.
"""

from flask import request

import state
from models.bahan_kajian import BahanKajian
from utils.response import success, created, not_found, error
from services.lock_guard import assert_periode_unlocked
from utils.pagination import get_pagination_params, apply_pagination
from middleware.validation import validate_request, validation_error_response


BK_SCHEMA = {
    "kode": {"required": True, "type": "str", "max_length": 10},
    "nama": {"required": True, "type": "str", "max_length": 200},
    "periode_id": {"required": True, "type": "int"},
}


def list_bk():
    """GET /api/bk"""
    page, page_size = get_pagination_params()
    periode_id = request.args.get("periode_id", type=int)

    query = state.db.query(BahanKajian)
    if periode_id:
        query = query.filter_by(periode_id=periode_id)

    query = query.order_by(BahanKajian.kode)
    items, total = apply_pagination(query, page, page_size)
    return success(data=[i.to_dict() for i in items])


def create_bk():
    """POST /api/bk"""
    data = request.get_json(silent=True)
    is_valid, errors = validate_request(data, BK_SCHEMA)
    if not is_valid:
        return validation_error_response(errors)

    try:
        assert_periode_unlocked(data.get("periode_id"))
    except ValueError as e:
        return error(str(e), status=423)

    bk = BahanKajian(
        periode_id=data["periode_id"],
        kode=data["kode"],
        nama=data["nama"],
        deskripsi=data.get("deskripsi"),
        kompetensi=data.get("kompetensi"),
        referensi=data.get("referensi"),
    )
    state.db.add(bk)
    state.db.commit()
    return created(data=bk.to_dict())


def update_bk(record_id):
    """PUT /api/bk/<id>"""
    bk = state.db.query(BahanKajian).get(record_id)
    if bk is None:
        return not_found()

    try:
        assert_periode_unlocked(bk.periode_id)
    except ValueError as e:
        return error(str(e), status=423)

    data = request.get_json(silent=True)
    for field in ("kode", "nama", "deskripsi", "kompetensi", "referensi"):
        value = data.get(field)
        if value is not None:
            setattr(bk, field, value)

    state.db.commit()
    return success(data=bk.to_dict(), message="Data diperbarui")


def delete_bk(record_id):
    """DELETE /api/bk/<id>"""
    bk = state.db.query(BahanKajian).get(record_id)
    if bk is None:
        return not_found()

    try:
        assert_periode_unlocked(bk.periode_id)
    except ValueError as e:
        return error(str(e), status=423)

    state.db.delete(bk)
    state.db.commit()
    return success(message="Data dihapus")


ROUTE_DEFINITIONS = [
    ("GET", "/api/bk", list_bk, "view_kurikulum"),
    ("POST", "/api/bk", create_bk, "manage_master"),
    ("PUT", "/api/bk/<int:record_id>", update_bk, "manage_master"),
    ("DELETE", "/api/bk/<int:record_id>", delete_bk, "manage_master"),
]
