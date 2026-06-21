"""
CRUD Mata Kuliah (MK).
Tabel 9 Buku Panduan APTIKOM.
"""

from flask import request

import state
from models.mata_kuliah import MataKuliah
from utils.response import success, created, not_found, error
from services.lock_guard import assert_periode_unlocked
from utils.pagination import get_pagination_params, apply_pagination
from middleware.validation import validate_request, validation_error_response


MK_SCHEMA = {
    "kode": {"required": True, "type": "str", "max_length": 10},
    "nama": {"required": True, "type": "str", "max_length": 200},
    "sks": {"required": True, "type": "int", "min": 1, "max": 12},
    "semester": {"required": True, "type": "int", "min": 1, "max": 8},
    "periode_id": {"required": True, "type": "int"},
}


def list_mk():
    """GET /api/mk"""
    page, page_size = get_pagination_params()
    periode_id = request.args.get("periode_id", type=int)
    semester = request.args.get("semester", type=int)

    query = state.db.query(MataKuliah)
    if periode_id:
        query = query.filter_by(periode_id=periode_id)
    if semester:
        query = query.filter_by(semester=semester)

    query = query.order_by(MataKuliah.semester, MataKuliah.kode)
    items, total = apply_pagination(query, page, page_size)
    return success(data=[i.to_dict() for i in items])


def create_mk():
    """POST /api/mk"""
    data = request.get_json(silent=True)
    is_valid, errors = validate_request(data, MK_SCHEMA)
    if not is_valid:
        return validation_error_response(errors)

    try:
        assert_periode_unlocked(data.get("periode_id"))
    except ValueError as e:
        return error(str(e), status=423)

    mk = MataKuliah(
        periode_id=data["periode_id"],
        kode=data["kode"],
        nama=data["nama"],
        sks=data["sks"],
        semester=data["semester"],
        jenis=data.get("jenis", "wajib"),
        is_capstone=data.get("is_capstone", False),
        prasyarat=data.get("prasyarat"),
        deskripsi_singkat=data.get("deskripsi_singkat"),
        referensi=data.get("referensi"),
        ref_buku=data.get("ref_buku"),
        ref_spreadsheet=data.get("ref_spreadsheet"),
        ref_pikobe=data.get("ref_pikobe"),
    )
    state.db.add(mk)
    state.db.commit()
    return created(data=mk.to_dict())


def update_mk(record_id):
    """PUT /api/mk/<id>"""
    mk = state.db.query(MataKuliah).get(record_id)
    if mk is None:
        return not_found()

    try:
        assert_periode_unlocked(mk.periode_id)
    except ValueError as e:
        return error(str(e), status=423)

    data = request.get_json(silent=True)
    updatable = ("kode", "nama", "sks", "semester", "jenis",
                 "is_capstone", "prasyarat", "deskripsi_singkat",
                 "referensi", "ref_buku", "ref_spreadsheet", "ref_pikobe")
    for field in updatable:
        value = data.get(field)
        if value is not None:
            setattr(mk, field, value)

    state.db.commit()
    return success(data=mk.to_dict(), message="Data diperbarui")


def delete_mk(record_id):
    """DELETE /api/mk/<id>"""
    mk = state.db.query(MataKuliah).get(record_id)
    if mk is None:
        return not_found()

    try:
        assert_periode_unlocked(mk.periode_id)
    except ValueError as e:
        return error(str(e), status=423)

    state.db.delete(mk)
    state.db.commit()
    return success(message="Data dihapus")


ROUTE_DEFINITIONS = [
    ("GET", "/api/mk", list_mk, "view_kurikulum"),
    ("POST", "/api/mk", create_mk, "manage_master"),
    ("PUT", "/api/mk/<int:record_id>", update_mk, "manage_master"),
    ("DELETE", "/api/mk/<int:record_id>", delete_mk, "manage_master"),
]
