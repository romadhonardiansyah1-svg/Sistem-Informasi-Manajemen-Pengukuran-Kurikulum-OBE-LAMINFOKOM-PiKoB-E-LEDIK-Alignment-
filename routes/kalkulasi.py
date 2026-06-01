"""
API kalkulasi berjenjang.
Menjalankan pipeline: Nilai -> CPMK -> MK -> CPL -> PL.
"""

from flask import request

import state
from services.kalkulasi_engine import (
    hitung_nilai_mk, hitung_nilai_cpl, hitung_seluruh_mahasiswa,
)
from utils.response import success, error


def kalkulasi_mk():
    """POST /api/kalkulasi/mk"""
    data = request.get_json(silent=True)
    mahasiswa_id = data.get("mahasiswa_id")
    mk_id = data.get("mk_id")

    result = hitung_nilai_mk(mahasiswa_id, mk_id)
    return success(data=result)


def kalkulasi_cpl():
    """POST /api/kalkulasi/cpl"""
    data = request.get_json(silent=True)
    mahasiswa_id = data.get("mahasiswa_id")
    cpl_id = data.get("cpl_id")

    result = hitung_nilai_cpl(mahasiswa_id, cpl_id)
    return success(data=result)


def kalkulasi_full():
    """POST /api/kalkulasi/full"""
    data = request.get_json(silent=True)
    mahasiswa_id = data.get("mahasiswa_id")

    result = hitung_seluruh_mahasiswa(mahasiswa_id)
    return success(data=result)


ROUTE_DEFINITIONS = [
    ("POST", "/api/kalkulasi/mk", kalkulasi_mk, "view_report"),
    ("POST", "/api/kalkulasi/cpl", kalkulasi_cpl, "view_report"),
    ("POST", "/api/kalkulasi/full", kalkulasi_full, "view_report"),
]
