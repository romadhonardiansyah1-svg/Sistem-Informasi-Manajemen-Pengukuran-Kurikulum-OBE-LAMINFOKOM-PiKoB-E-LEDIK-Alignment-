"""
Route identitas prodi (Tabel A Buku Panduan APTIKOM).
GET dan PUT profil program studi aktif.
"""

from flask import request

import state
from models.institution import Universitas, Fakultas, ProgramStudi
from models.period import PeriodeKurikulum
from utils.response import success, not_found


def get_identitas_prodi():
    """GET /api/identitas-prodi"""
    prodi = state.db.query(ProgramStudi).first()
    if prodi is None:
        return not_found("Data program studi belum tersedia")

    fakultas = state.db.query(Fakultas).get(prodi.fakultas_id)
    univ = state.db.query(Universitas).get(fakultas.universitas_id) if fakultas else None

    periode_aktif = (
        state.db.query(PeriodeKurikulum)
        .filter_by(prodi_id=prodi.id, status="aktif")
        .first()
    )

    data = {
        "prodi": prodi.to_dict(),
        "fakultas": fakultas.to_dict() if fakultas else None,
        "universitas": univ.to_dict() if univ else None,
        "periode_aktif": periode_aktif.to_dict() if periode_aktif else None,
    }
    return success(data=data)


def update_identitas_prodi():
    """PUT /api/identitas-prodi"""
    payload = request.get_json(silent=True)

    prodi = state.db.query(ProgramStudi).first()
    if prodi is None:
        return not_found("Data program studi belum tersedia")

    prodi_fields = ("nama", "jenjang", "akreditasi", "visi", "misi", "website", "email", "gelar_lulusan")
    for field in prodi_fields:
        val = payload.get(field)
        if val is not None:
            setattr(prodi, field, val)

    fak_nama = payload.get("fakultas_nama")
    if fak_nama:
        fakultas = state.db.query(Fakultas).get(prodi.fakultas_id)
        if fakultas:
            fakultas.nama = fak_nama

    univ_nama = payload.get("universitas_nama")
    univ_alamat = payload.get("universitas_alamat")
    if univ_nama or univ_alamat:
        fakultas = state.db.query(Fakultas).get(prodi.fakultas_id)
        if fakultas:
            univ = state.db.query(Universitas).get(fakultas.universitas_id)
            if univ:
                if univ_nama:
                    univ.nama = univ_nama
                if univ_alamat:
                    univ.alamat = univ_alamat

    state.db.commit()
    return success(message="Identitas prodi diperbarui")


ROUTE_DEFINITIONS = [
    ("GET", "/api/identitas-prodi", get_identitas_prodi, "view_kurikulum"),
    ("PUT", "/api/identitas-prodi", update_identitas_prodi, "manage_prodi"),
]
