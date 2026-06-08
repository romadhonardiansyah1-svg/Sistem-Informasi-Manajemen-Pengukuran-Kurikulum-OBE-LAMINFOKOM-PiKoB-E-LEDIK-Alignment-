"""
CRUD CPL Prodi dan CPL SN-Dikti.
Tabel 2 dan 4 Buku Panduan APTIKOM.
"""

from flask import request

import state
from models.cpl import CPLProdi, CPLSNDikti
from utils.response import success, created, not_found
from utils.pagination import get_pagination_params, apply_pagination
from middleware.validation import validate_request, validation_error_response


CPL_PRODI_SCHEMA = {
    "kode": {"required": True, "type": "str", "max_length": 10},
    "deskripsi": {"required": True, "type": "str"},
    "periode_id": {"required": True, "type": "int"},
}

CPL_SNDIKTI_SCHEMA = {
    "kode": {"required": True, "type": "str", "max_length": 20},
    "kategori": {"required": True, "type": "str", "choices": ("S", "KU", "KK", "P")},
    "deskripsi": {"required": True, "type": "str"},
    "periode_id": {"required": True, "type": "int"},
}


def list_cpl_prodi():
    """GET /api/cpl-prodi"""
    page, page_size = get_pagination_params()
    periode_id = request.args.get("periode_id", type=int)

    query = state.db.query(CPLProdi)
    if periode_id:
        query = query.filter_by(periode_id=periode_id)

    query = query.order_by(CPLProdi.kode)
    items, total = apply_pagination(query, page, page_size)
    return success(data=[i.to_dict() for i in items])


def create_cpl_prodi():
    """POST /api/cpl-prodi"""
    data = request.get_json(silent=True)
    is_valid, errors = validate_request(data, CPL_PRODI_SCHEMA)
    if not is_valid:
        return validation_error_response(errors)

    cpl = CPLProdi(
        periode_id=data["periode_id"],
        kode=data["kode"],
        deskripsi=data["deskripsi"],
        referensi=data.get("referensi"),
    )
    state.db.add(cpl)
    state.db.commit()
    return created(data=cpl.to_dict())


def update_cpl_prodi(record_id):
    """PUT /api/cpl-prodi/<id>"""
    cpl = state.db.query(CPLProdi).get(record_id)
    if cpl is None:
        return not_found()

    data = request.get_json(silent=True)
    for field in ("kode", "deskripsi", "referensi"):
        value = data.get(field)
        if value is not None:
            setattr(cpl, field, value)

    state.db.commit()
    return success(data=cpl.to_dict(), message="Data diperbarui")


def delete_cpl_prodi(record_id):
    """DELETE /api/cpl-prodi/<id>"""
    cpl = state.db.query(CPLProdi).get(record_id)
    if cpl is None:
        return not_found()

    state.db.delete(cpl)
    state.db.commit()
    return success(message="Data dihapus")


def list_cpl_sndikti():
    """GET /api/cpl-sndikti"""
    page, page_size = get_pagination_params()
    periode_id = request.args.get("periode_id", type=int)

    query = state.db.query(CPLSNDikti)
    if periode_id:
        query = query.filter_by(periode_id=periode_id)

    query = query.order_by(CPLSNDikti.kode)
    items, total = apply_pagination(query, page, page_size)
    return success(data=[i.to_dict() for i in items])


def create_cpl_sndikti():
    """POST /api/cpl-sndikti"""
    data = request.get_json(silent=True)
    is_valid, errors = validate_request(data, CPL_SNDIKTI_SCHEMA)
    if not is_valid:
        return validation_error_response(errors)

    cpl = CPLSNDikti(
        periode_id=data["periode_id"],
        kode=data["kode"],
        kategori=data["kategori"],
        deskripsi=data["deskripsi"],
        referensi=data.get("referensi"),
    )
    state.db.add(cpl)
    state.db.commit()
    return created(data=cpl.to_dict())


ROUTE_DEFINITIONS = [
    ("GET", "/api/cpl-prodi", list_cpl_prodi, "view_kurikulum"),
    ("POST", "/api/cpl-prodi", create_cpl_prodi, "manage_master"),
    ("PUT", "/api/cpl-prodi/<int:record_id>", update_cpl_prodi, "manage_master"),
    ("DELETE", "/api/cpl-prodi/<int:record_id>", delete_cpl_prodi, "manage_master"),
    ("GET", "/api/cpl-sndikti", list_cpl_sndikti, "view_kurikulum"),
    ("POST", "/api/cpl-sndikti", create_cpl_sndikti, "manage_master"),
]
