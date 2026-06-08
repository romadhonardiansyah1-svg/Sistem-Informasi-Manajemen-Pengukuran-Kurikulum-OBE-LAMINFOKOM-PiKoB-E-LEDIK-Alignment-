"""
Pemetaan MK-CPMK-SubCPMK (Tabel 15 Buku Panduan APTIKOM).
Menampilkan per MK: CPL, CPMK, dan Sub-CPMK terkait.
"""

import state
from models.mata_kuliah import MataKuliah
from models.cpmk import CPMK
from models.sub_cpmk import SubCPMK
from models.cpl import CPLProdi
from models.mapping import mapping_cpmk_mk
from utils.response import success
from sqlalchemy import select


def get_pemetaan_mk_subcpmk():
    """GET /api/pemetaan-mk-subcpmk -- per MK."""
    session = state.db

    mks = session.query(MataKuliah).order_by(MataKuliah.kode).all()
    cpmk_mk_rows = session.execute(select(mapping_cpmk_mk)).fetchall()

    mk_cpmk_map = {}
    for row in cpmk_mk_rows:
        if row.mk_id not in mk_cpmk_map:
            mk_cpmk_map[row.mk_id] = []
        mk_cpmk_map[row.mk_id].append(row.cpmk_id)

    cpmk_all = session.query(CPMK).all()
    cpmk_dict = {}
    for c in cpmk_all:
        cpmk_dict[c.id] = c

    cpl_all = session.query(CPLProdi).all()
    cpl_dict = {}
    for c in cpl_all:
        cpl_dict[c.id] = c

    sub_all = session.query(SubCPMK).all()
    sub_by_cpmk = {}
    for s in sub_all:
        if s.cpmk_id not in sub_by_cpmk:
            sub_by_cpmk[s.cpmk_id] = []
        sub_by_cpmk[s.cpmk_id].append(s)

    result = []
    for mk in mks:
        cpmk_ids = mk_cpmk_map.get(mk.id, [])
        cpmk_entries = []
        for cpmk_id in cpmk_ids:
            cpmk = cpmk_dict.get(cpmk_id)
            if cpmk is None:
                continue
            cpl = cpl_dict.get(cpmk.cpl_id)
            subs = sub_by_cpmk.get(cpmk.id, [])
            cpmk_entries.append({
                "kode": cpmk.kode,
                "deskripsi": cpmk.deskripsi,
                "cpl_kode": cpl.kode if cpl else "",
                "sub_cpmk": [
                    {"kode": s.kode, "deskripsi": s.deskripsi}
                    for s in subs
                    if s.mk_id == mk.id
                ],
            })

        result.append({
            "kode": mk.kode,
            "nama": mk.nama,
            "semester": mk.semester,
            "cpmk": cpmk_entries,
        })

    return success(data=result)


ROUTE_DEFINITIONS = [
    ("GET", "/api/pemetaan-mk-subcpmk", get_pemetaan_mk_subcpmk, "view_kurikulum"),
]
