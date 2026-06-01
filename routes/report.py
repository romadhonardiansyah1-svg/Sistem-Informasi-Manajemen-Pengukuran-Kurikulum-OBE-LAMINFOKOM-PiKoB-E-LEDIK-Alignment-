"""
Route laporan dan visualisasi CPL.
"""

from flask import request

import state
from services.report_service import (
    get_cpl_report_mahasiswa,
    get_cpl_report_agregat,
)
from utils.response import success


def report_cpl_mahasiswa():
    """GET /api/report/cpl/mahasiswa"""
    mahasiswa_id = request.args.get("mahasiswa_id", type=int)
    result = get_cpl_report_mahasiswa(mahasiswa_id)
    return success(data=result)


def report_cpl_agregat():
    """GET /api/report/cpl/agregat"""
    angkatan = request.args.get("angkatan", type=int)
    periode_id = request.args.get("periode_id", type=int)
    result = get_cpl_report_agregat(angkatan, periode_id)
    return success(data=result)


ROUTE_DEFINITIONS = [
    ("GET", "/api/report/cpl/mahasiswa", report_cpl_mahasiswa, "view_report"),
    ("GET", "/api/report/cpl/agregat", report_cpl_agregat, "view_report"),
]
