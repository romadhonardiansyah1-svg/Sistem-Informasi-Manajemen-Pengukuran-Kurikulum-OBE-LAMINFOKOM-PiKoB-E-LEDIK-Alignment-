"""
Route CRUD ringkas untuk data master dropdown: Kategori PL dan Jenis MK.
GET/POST saja (list + create). Frontend mengonsumsi via <select> dropdown.
"""

from flask import request

import state
from models.master_dropdown import KategoriPL, JenisMK
from utils.response import success, created, error


def list_kategori_pl():
    """GET /api/kategori-pl"""
    items = state.db.query(KategoriPL).order_by(KategoriPL.id).all()
    return success(data=[i.to_dict() for i in items])


def create_kategori_pl():
    """POST /api/kategori-pl"""
    data = request.get_json(silent=True) or {}
    nama = (data.get("nama") or "").strip()
    if not nama:
        return error("Nama kategori wajib diisi.")
    item = KategoriPL(nama=nama)
    state.db.add(item)
    state.db.commit()
    return created(data=item.to_dict())


def delete_kategori_pl(record_id):
    """DELETE /api/kategori-pl/<id>"""
    item = state.db.query(KategoriPL).get(record_id)
    if item is None:
        return error("Data tidak ditemukan", status=404)
    state.db.delete(item)
    state.db.commit()
    return success(message="Kategori PL dihapus")


def list_jenis_mk():
    """GET /api/jenis-mk"""
    items = state.db.query(JenisMK).order_by(JenisMK.id).all()
    return success(data=[i.to_dict() for i in items])


def create_jenis_mk():
    """POST /api/jenis-mk"""
    data = request.get_json(silent=True) or {}
    nama = (data.get("nama") or "").strip()
    if not nama:
        return error("Nama jenis MK wajib diisi.")
    item = JenisMK(nama=nama)
    state.db.add(item)
    state.db.commit()
    return created(data=item.to_dict())


def delete_jenis_mk(record_id):
    """DELETE /api/jenis-mk/<id>"""
    item = state.db.query(JenisMK).get(record_id)
    if item is None:
        return error("Data tidak ditemukan", status=404)
    state.db.delete(item)
    state.db.commit()
    return success(message="Jenis MK dihapus")


ROUTE_DEFINITIONS = [
    ("GET", "/api/kategori-pl", list_kategori_pl, "view_kurikulum"),
    ("POST", "/api/kategori-pl", create_kategori_pl, "manage_master"),
    ("DELETE", "/api/kategori-pl/<int:record_id>", delete_kategori_pl, "manage_master"),
    ("GET", "/api/jenis-mk", list_jenis_mk, "view_kurikulum"),
    ("POST", "/api/jenis-mk", create_jenis_mk, "manage_master"),
    ("DELETE", "/api/jenis-mk/<int:record_id>", delete_jenis_mk, "manage_master"),
]
