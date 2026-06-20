"""
Route manajemen periode kurikulum.
"""

from flask import request

import config
import state
from models.period import PeriodeKurikulum
from utils.response import success, created, not_found


def _span():
    """Rentang tahun (inklusif) untuk satu periode = 5 tahun -> selisih 4."""
    return config.PERIODE_DURATION_YEARS - 1


def list_periode():
    """GET /api/periode"""
    prodi_id = request.args.get("prodi_id", type=int)
    query = state.db.query(PeriodeKurikulum)
    if prodi_id:
        query = query.filter_by(prodi_id=prodi_id)
    items = query.order_by(PeriodeKurikulum.tahun_mulai.desc()).all()
    return success(data=[i.to_dict() for i in items])


def create_periode():
    """
    POST /api/periode
    Periode kurikulum WAJIB 5 tahun. tahun_selesai dipaksa = tahun_mulai + 4
    agar konsisten meski input tidak sesuai. nama otomatis bila kosong.
    """
    data = request.get_json(silent=True) or {}
    tahun_mulai = int(data["tahun_mulai"])
    tahun_selesai = tahun_mulai + _span()  # selalu 5 tahun (inklusif)
    nama = data.get("nama") or ("Kurikulum " + str(tahun_mulai) + "-" + str(tahun_selesai))

    periode = PeriodeKurikulum(
        prodi_id=data["prodi_id"],
        nama=nama,
        tahun_mulai=tahun_mulai,
        tahun_selesai=tahun_selesai,
        status=data.get("status", "draft"),
    )
    state.db.add(periode)
    state.db.commit()
    return created(data=periode.to_dict())


def update_periode(record_id):
    """PUT /api/periode/<id>"""
    periode = state.db.query(PeriodeKurikulum).get(record_id)
    if periode is None:
        return not_found()

    data = request.get_json(silent=True) or {}
    for field in ("nama", "tahun_mulai", "tahun_selesai", "status", "locked"):
        value = data.get(field)
        if value is not None:
            setattr(periode, field, value)

    # Jaga invarian 5 tahun: tahun_selesai selalu mengikuti tahun_mulai.
    if periode.tahun_mulai is not None:
        periode.tahun_selesai = int(periode.tahun_mulai) + _span()

    state.db.commit()
    return success(data=periode.to_dict(), message="Periode diperbarui")


def lock_periode(record_id):
    """POST /api/periode/<id>/lock"""
    periode = state.db.query(PeriodeKurikulum).get(record_id)
    if periode is None:
        return not_found()

    periode.locked = True
    state.db.commit()
    return success(message="Periode dikunci")


def unlock_periode(record_id):
    """POST /api/periode/<id>/unlock"""
    periode = state.db.query(PeriodeKurikulum).get(record_id)
    if periode is None:
        return not_found()

    periode.locked = False
    state.db.commit()
    return success(message="Periode dibuka kuncinya")


ROUTE_DEFINITIONS = [
    ("GET", "/api/periode", list_periode, "view_kurikulum"),
    ("POST", "/api/periode", create_periode, "manage_periode"),
    ("PUT", "/api/periode/<int:record_id>", update_periode, "manage_periode"),
    ("POST", "/api/periode/<int:record_id>/lock", lock_periode, "lock_periode"),
    ("POST", "/api/periode/<int:record_id>/unlock", unlock_periode, "lock_periode"),
]
