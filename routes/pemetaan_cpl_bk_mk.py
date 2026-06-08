"""
Pemetaan CPL-BK-MK (Tabel 8 Buku Panduan APTIKOM).
Read-only gabungan view dari data BK-MK dan CPL-BK.
"""

import state
from models.cpl import CPLProdi
from models.bahan_kajian import BahanKajian
from models.mata_kuliah import MataKuliah
from models.mapping import mapping_cpl_bk, mapping_bk_mk
from utils.response import success
from sqlalchemy import select


def get_pemetaan_cpl_bk_mk():
    """GET /api/pemetaan-cpl-bk-mk -- gabungan view."""
    session = state.db

    cpls = session.query(CPLProdi).order_by(CPLProdi.kode).all()
    bks = session.query(BahanKajian).order_by(BahanKajian.kode).all()
    mks = session.query(MataKuliah).order_by(MataKuliah.kode).all()

    cpl_bk_rows = session.execute(select(mapping_cpl_bk)).fetchall()
    bk_mk_rows = session.execute(select(mapping_bk_mk)).fetchall()

    cpl_bk_set = set()
    for row in cpl_bk_rows:
        cpl_bk_set.add((row.cpl_id, row.bk_id))

    bk_mk_set = set()
    for row in bk_mk_rows:
        bk_mk_set.add((row.bk_id, row.mk_id))

    bk_map = {}
    for bk in bks:
        bk_map[bk.id] = bk.kode

    result = []
    for cpl in cpls:
        related_bks = []
        for bk in bks:
            is_linked = (cpl.id, bk.id) in cpl_bk_set
            if not is_linked:
                continue
            related_mks = []
            for mk in mks:
                if (bk.id, mk.id) in bk_mk_set:
                    related_mks.append({"kode": mk.kode, "nama": mk.nama})
            related_bks.append({
                "kode": bk.kode,
                "nama": bk.nama,
                "mata_kuliah": related_mks,
            })
        result.append({
            "kode": cpl.kode,
            "deskripsi": cpl.deskripsi,
            "bahan_kajian": related_bks,
        })

    return success(data=result)


ROUTE_DEFINITIONS = [
    ("GET", "/api/pemetaan-cpl-bk-mk", get_pemetaan_cpl_bk_mk, "view_kurikulum"),
]
