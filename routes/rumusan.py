"""
Rumusan Akhir MK dan CPL (Tabel 19 dan 20 Buku Panduan APTIKOM).
Kalkulasi skor per MK dan per CPL.
"""

import state
from models.mata_kuliah import MataKuliah
from models.cpl import CPLProdi
from models.cpmk import CPMK
from models.mapping import mapping_cpl_mk, mapping_cpmk_mk
from utils.response import success
from sqlalchemy import select


def get_rumusan_mk():
    """GET /api/rumusan-mk -- Tabel 19. Rumusan Akhir MK."""
    session = state.db

    mks = session.query(MataKuliah).order_by(MataKuliah.kode).all()
    cpls = session.query(CPLProdi).all()
    cpmks = session.query(CPMK).all()

    cpl_dict = {}
    for c in cpls:
        cpl_dict[c.id] = c

    cpl_mk_rows = session.execute(select(mapping_cpl_mk)).fetchall()
    cpmk_mk_rows = session.execute(select(mapping_cpmk_mk)).fetchall()

    mk_cpls = {}
    for row in cpl_mk_rows:
        if row.mk_id not in mk_cpls:
            mk_cpls[row.mk_id] = set()
        mk_cpls[row.mk_id].add(row.cpl_id)

    mk_cpmks = {}
    for row in cpmk_mk_rows:
        if row.mk_id not in mk_cpmks:
            mk_cpmks[row.mk_id] = set()
        mk_cpmks[row.mk_id].add(row.cpmk_id)

    cpmk_by_id = {}
    for c in cpmks:
        cpmk_by_id[c.id] = c

    result = []
    for mk in mks:
        cpl_ids = mk_cpls.get(mk.id, set())
        cpmk_ids = mk_cpmks.get(mk.id, set())
        cpmk_kodes = []
        for cid in cpmk_ids:
            c = cpmk_by_id.get(cid)
            if c:
                cpmk_kodes.append(c.kode)
        cpl_kodes = []
        for cid in cpl_ids:
            c = cpl_dict.get(cid)
            if c:
                cpl_kodes.append(c.kode)

        skor_maks = len(cpmk_ids) * 100
        result.append({
            "kode": mk.kode,
            "nama": mk.nama,
            "cpl": sorted(cpl_kodes),
            "cpmk": sorted(cpmk_kodes),
            "skor_maks": skor_maks,
            "total": skor_maks,
        })

    return success(data=result)


def get_rumusan_cpl():
    """GET /api/rumusan-cpl -- Tabel 20. Rumusan Akhir CPL."""
    session = state.db

    cpls = session.query(CPLProdi).order_by(CPLProdi.kode).all()
    mks = session.query(MataKuliah).all()
    cpmks = session.query(CPMK).all()

    mk_dict = {}
    for m in mks:
        mk_dict[m.id] = m

    cpl_mk_rows = session.execute(select(mapping_cpl_mk)).fetchall()
    cpmk_mk_rows = session.execute(select(mapping_cpmk_mk)).fetchall()

    cpl_mks = {}
    for row in cpl_mk_rows:
        if row.cpl_id not in cpl_mks:
            cpl_mks[row.cpl_id] = set()
        cpl_mks[row.cpl_id].add(row.mk_id)

    cpmk_by_cpl = {}
    for c in cpmks:
        if c.cpl_id not in cpmk_by_cpl:
            cpmk_by_cpl[c.cpl_id] = []
        cpmk_by_cpl[c.cpl_id].append(c)

    result = []
    for cpl in cpls:
        mk_ids = cpl_mks.get(cpl.id, set())
        mk_kodes = sorted(
            mk_dict[mid].kode for mid in mk_ids if mid in mk_dict
        )
        cpmk_list = cpmk_by_cpl.get(cpl.id, [])
        cpmk_kodes = sorted(c.kode for c in cpmk_list)
        skor_maks = len(cpmk_list) * 100

        result.append({
            "kode": cpl.kode,
            "deskripsi": cpl.deskripsi,
            "mk": mk_kodes,
            "cpmk": cpmk_kodes,
            "skor_maks": skor_maks,
            "total": skor_maks,
        })

    return success(data=result)


ROUTE_DEFINITIONS = [
    ("GET", "/api/rumusan-mk", get_rumusan_mk, "view_all"),
    ("GET", "/api/rumusan-cpl", get_rumusan_cpl, "view_all"),
]
