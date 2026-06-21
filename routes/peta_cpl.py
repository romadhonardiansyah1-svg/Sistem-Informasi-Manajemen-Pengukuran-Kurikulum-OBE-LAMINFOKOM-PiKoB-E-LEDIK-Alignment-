"""
Peta Pemenuhan CPL (Tabel 11 Buku Panduan APTIKOM).
Diturunkan OTOMATIS dari mapping_cpl_mk JOIN master_mata_kuliah.semester_penempatan.
Bentuk: baris = CPL, kolom = Semester 1..8, isi sel = daftar MK + jumlah SKS.
"""

import state
from flask import request
from models.cpl import CPLProdi
from models.mata_kuliah import MataKuliah
from models.mapping import mapping_cpl_mk
from utils.response import success
from services.periode_helper import resolve_periode_id
from sqlalchemy import select


def get_peta_cpl():
    """GET /api/peta-cpl -- CPL per semester (otomatis dari relasi)."""
    session = state.db
    periode_id = resolve_periode_id()

    cpl_q = session.query(CPLProdi)
    mk_q = session.query(MataKuliah)
    if periode_id:
        cpl_q = cpl_q.filter_by(periode_id=periode_id)
        mk_q = mk_q.filter_by(periode_id=periode_id)

    cpls = cpl_q.order_by(CPLProdi.kode).all()
    mks = mk_q.order_by(MataKuliah.kode).all()

    mk_dict = {}
    for mk in mks:
        mk_dict[mk.id] = {"kode": mk.kode, "nama": mk.nama, "sks": mk.sks, "semester": mk.semester}

    cpl_mk_rows = session.execute(select(mapping_cpl_mk)).fetchall()

    # Bangun mapping cpl_id -> semester -> list of MK
    cpl_sem_mks = {}
    for row in cpl_mk_rows:
        cpl_id = row.cpl_id
        mk_info = mk_dict.get(row.mk_id)
        if mk_info is None:
            continue
        sem = mk_info["semester"]
        key = (cpl_id, sem)
        if key not in cpl_sem_mks:
            cpl_sem_mks[key] = []
        cpl_sem_mks[key].append(mk_info)

    all_semesters = sorted(set(mk["semester"] for mk in mk_dict.values()))

    result = []
    for cpl in cpls:
        sem_data = {}
        for sem in all_semesters:
            mk_list = cpl_sem_mks.get((cpl.id, sem), [])
            total_sks = sum(m["sks"] for m in mk_list)
            sem_data[str(sem)] = {
                "count": len(mk_list),
                "sks": total_sks,
                "mk_list": [{"kode": m["kode"], "nama": m["nama"], "sks": m["sks"]} for m in mk_list],
            }
        result.append({
            "kode": cpl.kode,
            "deskripsi": cpl.deskripsi,
            "semesters": sem_data,
        })

    return success(data={"semesters": all_semesters, "rows": result})


ROUTE_DEFINITIONS = [
    ("GET", "/api/peta-cpl", get_peta_cpl, "view_kurikulum"),
]
