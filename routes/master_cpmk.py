"""
CRUD CPMK dan Sub-CPMK.
Tabel 12, 13, 14, 15 Buku Panduan APTIKOM.
"""

from flask import request

import state
from models.cpmk import CPMK
from models.sub_cpmk import SubCPMK
from utils.response import success, created, not_found, error
from services.lock_guard import assert_periode_unlocked
from models.cpl import CPLProdi
from utils.pagination import get_pagination_params, apply_pagination
from middleware.validation import validate_request, validation_error_response


CPMK_SCHEMA = {
    "kode": {"required": True, "type": "str", "max_length": 20},
    "deskripsi": {"required": True, "type": "str"},
    "cpl_id": {"required": True, "type": "int"},
}

SUB_CPMK_SCHEMA = {
    "kode": {"required": True, "type": "str", "max_length": 30},
    "deskripsi": {"required": True, "type": "str"},
    "cpmk_id": {"required": True, "type": "int"},
    "mk_id": {"required": True, "type": "int"},
}


def _periode_id_of_cpl(cpl_id):
    """Resolve periode_id dari CPL induk."""
    if not cpl_id:
        return None
    cpl = state.db.query(CPLProdi).get(cpl_id)
    return cpl.periode_id if cpl else None


def list_cpmk():
    """GET /api/cpmk"""
    page, page_size = get_pagination_params()
    cpl_id = request.args.get("cpl_id", type=int)

    query = state.db.query(CPMK)
    if cpl_id:
        query = query.filter_by(cpl_id=cpl_id)

    query = query.order_by(CPMK.kode)
    items, total = apply_pagination(query, page, page_size)
    return success(data=[i.to_dict() for i in items])


def create_cpmk():
    """POST /api/cpmk"""
    data = request.get_json(silent=True)
    is_valid, errors = validate_request(data, CPMK_SCHEMA)
    if not is_valid:
        return validation_error_response(errors)

    cpmk = CPMK(
        cpl_id=data["cpl_id"],
        kode=data["kode"],
        deskripsi=data["deskripsi"],
    )

    try:
        assert_periode_unlocked(_periode_id_of_cpl(data["cpl_id"]))
    except ValueError as e:
        return error(str(e), status=423)

    state.db.add(cpmk)
    state.db.commit()
    return created(data=cpmk.to_dict())


def update_cpmk(record_id):
    """PUT /api/cpmk/<id>"""
    cpmk = state.db.query(CPMK).get(record_id)
    if cpmk is None:
        return not_found()

    try:
        assert_periode_unlocked(_periode_id_of_cpl(cpmk.cpl_id))
    except ValueError as e:
        return error(str(e), status=423)

    data = request.get_json(silent=True)
    for field in ("kode", "deskripsi"):
        value = data.get(field)
        if value is not None:
            setattr(cpmk, field, value)

    state.db.commit()
    return success(data=cpmk.to_dict(), message="Data diperbarui")


def delete_cpmk(record_id):
    """DELETE /api/cpmk/<id>"""
    cpmk = state.db.query(CPMK).get(record_id)
    if cpmk is None:
        return not_found()

    try:
        assert_periode_unlocked(_periode_id_of_cpl(cpmk.cpl_id))
    except ValueError as e:
        return error(str(e), status=423)

    state.db.delete(cpmk)
    state.db.commit()
    return success(message="Data dihapus")


def list_sub_cpmk():
    """GET /api/sub-cpmk"""
    page, page_size = get_pagination_params()
    cpmk_id = request.args.get("cpmk_id", type=int)
    mk_id = request.args.get("mk_id", type=int)

    query = state.db.query(SubCPMK)
    if cpmk_id:
        query = query.filter_by(cpmk_id=cpmk_id)
    if mk_id:
        query = query.filter_by(mk_id=mk_id)

    query = query.order_by(SubCPMK.kode)
    items, total = apply_pagination(query, page, page_size)
    return success(data=[i.to_dict() for i in items])


def create_sub_cpmk():
    """POST /api/sub-cpmk"""
    data = request.get_json(silent=True)
    is_valid, errors = validate_request(data, SUB_CPMK_SCHEMA)
    if not is_valid:
        return validation_error_response(errors)

    sub = SubCPMK(
        cpmk_id=data["cpmk_id"],
        mk_id=data["mk_id"],
        kode=data["kode"],
        deskripsi=data["deskripsi"],
    )
    state.db.add(sub)
    state.db.commit()
    return created(data=sub.to_dict())


ROUTE_DEFINITIONS = [
    ("GET", "/api/cpmk", list_cpmk, "view_kurikulum"),
    ("POST", "/api/cpmk", create_cpmk, "manage_master"),
    ("PUT", "/api/cpmk/<int:record_id>", update_cpmk, "manage_master"),
    ("DELETE", "/api/cpmk/<int:record_id>", delete_cpmk, "manage_master"),
    ("GET", "/api/sub-cpmk", list_sub_cpmk, "view_kurikulum"),
    ("POST", "/api/sub-cpmk", create_sub_cpmk, "manage_master"),
]
