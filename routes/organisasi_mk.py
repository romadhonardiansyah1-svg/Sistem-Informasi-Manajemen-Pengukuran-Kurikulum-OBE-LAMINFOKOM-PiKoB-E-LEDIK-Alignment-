"""
Organisasi Mata Kuliah (Tabel 10 Buku Panduan APTIKOM).
Menampilkan MK per semester dalam layout visual.
"""

import state
from models.mata_kuliah import MataKuliah
from utils.response import success


def get_organisasi_mk():
    """GET /api/organisasi-mk -- MK dikelompokkan per semester."""
    session = state.db
    mks = session.query(MataKuliah).order_by(
        MataKuliah.semester, MataKuliah.kode
    ).all()

    semesters = {}
    for mk in mks:
        sem = mk.semester
        if sem not in semesters:
            semesters[sem] = []
        semesters[sem].append({
            "id": mk.id,
            "kode": mk.kode,
            "nama": mk.nama,
            "sks": mk.sks,
            "jenis": mk.jenis,
        })

    result = []
    for sem_num in sorted(semesters.keys()):
        total_sks = sum(m["sks"] for m in semesters[sem_num])
        result.append({
            "semester": sem_num,
            "total_sks": total_sks,
            "mata_kuliah": semesters[sem_num],
        })

    return success(data=result)


ROUTE_DEFINITIONS = [
    ("GET", "/api/organisasi-mk", get_organisasi_mk, "view_all"),
]
