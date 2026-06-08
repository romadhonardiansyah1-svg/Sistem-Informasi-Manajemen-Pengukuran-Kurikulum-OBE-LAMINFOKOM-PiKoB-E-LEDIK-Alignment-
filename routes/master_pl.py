"""
CRUD Profil Lulusan (PL).
Tabel 1 Buku Panduan APTIKOM.
"""

from flask import request

import state
from models.profil_lulusan import ProfilLulusan
from utils.response import success, created, not_found, error
from utils.pagination import get_pagination_params, apply_pagination
from middleware.validation import validate_request, validation_error_response


PL_SCHEMA = {
    "kode": {"required": True, "type": "str", "max_length": 10},
    "deskripsi": {"required": True, "type": "str"},
    "periode_id": {"required": True, "type": "int"},
}


def list_pl():
    """GET /api/pl"""
    page, page_size = get_pagination_params()
    periode_id = request.args.get("periode_id", type=int)

    query = state.db.query(ProfilLulusan)
    if periode_id:
        query = query.filter_by(periode_id=periode_id)

    query = query.order_by(ProfilLulusan.kode)
    items, total = apply_pagination(query, page, page_size)
    return success(data=[i.to_dict() for i in items])


def create_pl():
    """POST /api/pl"""
    data = request.get_json(silent=True)
    is_valid, errors = validate_request(data, PL_SCHEMA)
    if not is_valid:
        return validation_error_response(errors)

    pl = ProfilLulusan(
        periode_id=data["periode_id"],
        kode=data["kode"],
        deskripsi=data["deskripsi"],
        kategori=data.get("kategori"),
        referensi=data.get("referensi"),
    )
    state.db.add(pl)
    state.db.commit()
    return created(data=pl.to_dict())


def update_pl(record_id):
    """PUT /api/pl/<id>"""
    pl = state.db.query(ProfilLulusan).get(record_id)
    if pl is None:
        return not_found()

    data = request.get_json(silent=True)
    updatable = ("kode", "deskripsi", "kategori", "referensi")
    for field in updatable:
        value = data.get(field)
        if value is not None:
            setattr(pl, field, value)

    state.db.commit()
    return success(data=pl.to_dict(), message="Data diperbarui")


def delete_pl(record_id):
    """DELETE /api/pl/<id>"""
    pl = state.db.query(ProfilLulusan).get(record_id)
    if pl is None:
        return not_found()

    state.db.delete(pl)
    state.db.commit()
    return success(message="Data dihapus")


ROUTE_DEFINITIONS = [
    ("GET", "/api/pl", list_pl, "view_kurikulum"),
    ("POST", "/api/pl", create_pl, "manage_master"),
    ("PUT", "/api/pl/<int:record_id>", update_pl, "manage_master"),
    ("DELETE", "/api/pl/<int:record_id>", delete_pl, "manage_master"),
]
