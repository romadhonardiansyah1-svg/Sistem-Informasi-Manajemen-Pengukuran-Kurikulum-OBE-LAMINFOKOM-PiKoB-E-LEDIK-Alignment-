"""
Peta Pemenuhan CPL (Tabel 11 Buku Panduan APTIKOM).
Menampilkan distribusi CPL per semester.
"""

import state
from models.cpl import CPLProdi
from models.mata_kuliah import MataKuliah
from models.mapping import mapping_cpl_mk
from utils.response import success
from sqlalchemy import select


def get_peta_cpl():
    """GET /api/peta-cpl -- CPL per semester."""
    session = state.db

    cpls = session.query(CPLProdi).order_by(CPLProdi.kode).all()
    mks = session.query(MataKuliah).order_by(MataKuliah.kode).all()

    mk_sem = {}
    for mk in mks:
        mk_sem[mk.id] = mk.semester

    cpl_mk_rows = session.execute(select(mapping_cpl_mk)).fetchall()

    cpl_semesters = {}
    for row in cpl_mk_rows:
        cpl_id = row.cpl_id
        sem = mk_sem.get(row.mk_id)
        if sem is None:
            continue
        key = (cpl_id, sem)
        if key not in cpl_semesters:
            cpl_semesters[key] = 0
        cpl_semesters[key] += 1

    all_semesters = sorted(set(mk.semester for mk in mks))

    result = []
    for cpl in cpls:
        sem_data = {}
        for sem in all_semesters:
            count = cpl_semesters.get((cpl.id, sem), 0)
            sem_data[str(sem)] = count
        result.append({
            "kode": cpl.kode,
            "deskripsi": cpl.deskripsi,
            "semesters": sem_data,
        })

    return success(data={"semesters": all_semesters, "rows": result})


ROUTE_DEFINITIONS = [
    ("GET", "/api/peta-cpl", get_peta_cpl, "view_all"),
]
