"""
Seed mapping CPMK ke MK dari Sheet 13. Pemetaan CPL-CPMK-MK.
Juga seed mapping CPL-MK dari Sheet 9.
"""

import state
from models.cpmk import CPMK
from models.cpl import CPLProdi
from models.mata_kuliah import MataKuliah
from models.mapping import mapping_cpmk_mk, mapping_cpl_mk


CPMK_MK_DATA = [
    ("CPMK011", ["MK04", "MK06"]),
    ("CPMK012", ["MK04"]),
    ("CPMK021", ["MK21", "MK32"]),
    ("CPMK022", ["MK07", "MK10", "MK11", "MK21", "MK32"]),
    ("CPMK031", ["MK19", "MK34", "MK29"]),
    ("CPMK032", ["MK05", "MK12", "MK18", "MK19", "MK20", "MK22", "MK29", "MK34", "MK47", "MK49"]),
    ("CPMK033", ["MK19", "MK22", "MK34"]),
    ("CPMK041", ["MK06", "MK13", "MK27", "MK48", "MK50", "MK51"]),
    ("CPMK042", ["MK31", "MK48"]),
    ("CPMK051", ["MK39", "MK42"]),
    ("CPMK052", ["MK39", "MK40", "MK42", "MK43", "MK44", "MK45", "MK46"]),
    ("CPMK061", ["MK14", "MK30", "MK33", "MK37", "MK38", "MK52", "MK53", "MK54", "MK55", "MK56"]),
    ("CPMK062", ["MK30", "MK33", "MK37", "MK38", "MK52", "MK53", "MK54", "MK55", "MK56"]),
    ("CPMK063", ["MK30", "MK33", "MK38", "MK52", "MK53", "MK54", "MK55", "MK56"]),
    ("CPMK064", ["MK54", "MK55", "MK56"]),
    ("CPMK071", ["MK23"]),
    ("CPMK072", ["MK23"]),
    ("CPMK073", ["MK23", "MK34", "MK40", "MK43", "MK44", "MK45"]),
    ("CPMK081", ["MK11", "MK24", "MK28", "MK32", "MK35"]),
    ("CPMK082", ["MK32", "MK57", "MK58", "MK59", "MK60", "MK61"]),
    ("CPMK091", ["MK15", "MK16", "MK17", "MK25", "MK26"]),
    ("CPMK092", ["MK15", "MK25", "MK26", "MK62", "MK63", "MK64", "MK65", "MK66"]),
    ("CPMK101", ["MK01", "MK08"]),
    ("CPMK102", ["MK02", "MK09", "MK42"]),
    ("CPMK111", ["MK02", "MK09", "MK16", "MK42"]),
    ("CPMK112", ["MK42"]),
    ("CPMK121", ["MK40", "MK43", "MK44"]),
    ("CPMK122", ["MK10", "MK40", "MK43", "MK44"]),
    ("CPMK131", ["MK40", "MK41", "MK43", "MK44", "MK45", "MK46"]),
    ("CPMK132", ["MK03", "MK36", "MK40", "MK41", "MK43", "MK44", "MK45", "MK46"]),
    ("CPMK133", ["MK40", "MK43", "MK44", "MK45", "MK46"]),
    ("CPMK141", ["MK40", "MK43", "MK44"]),
    ("CPMK142", ["MK40", "MK43", "MK44"]),
]


def _build_map(model, field):
    """Buat map kode -> id."""
    result = {}
    for row in state.db.query(model).all():
        result[getattr(row, field)] = row.id
    return result


def seed_cpmk_mk_matrix():
    """Seed mapping CPMK ke MK."""
    cpmk_map = _build_map(CPMK, "kode")
    mk_map = _build_map(MataKuliah, "kode")

    for cpmk_kode, mk_list in CPMK_MK_DATA:
        cpmk_id = cpmk_map.get(cpmk_kode)
        if cpmk_id is None:
            continue
        for mk_kode in mk_list:
            mk_id = mk_map.get(mk_kode)
            if mk_id is None:
                continue
            state.db.execute(
                mapping_cpmk_mk.insert().values(
                    cpmk_id=cpmk_id, mk_id=mk_id
                )
            )
    state.db.flush()


CPL_MK_DATA = [
    ("CPL01", ["MK04", "MK06"]),
    ("CPL02", ["MK07", "MK10", "MK11", "MK12", "MK21", "MK32"]),
    ("CPL03", ["MK05", "MK12", "MK18", "MK19", "MK20", "MK22", "MK29", "MK34", "MK47", "MK49"]),
    ("CPL04", ["MK06", "MK13", "MK27", "MK31", "MK48", "MK50", "MK51"]),
    ("CPL05", ["MK39", "MK40", "MK42", "MK43", "MK44", "MK45", "MK46"]),
    ("CPL06", ["MK14", "MK30", "MK33", "MK37", "MK38", "MK52", "MK53", "MK54", "MK55", "MK56"]),
    ("CPL07", ["MK23", "MK34", "MK40", "MK43", "MK44", "MK45"]),
    ("CPL08", ["MK11", "MK24", "MK28", "MK32", "MK35", "MK57", "MK58", "MK59", "MK60", "MK61"]),
    ("CPL09", ["MK15", "MK16", "MK17", "MK25", "MK26", "MK62", "MK63", "MK64", "MK65", "MK66"]),
    ("CPL10", ["MK01", "MK02", "MK08", "MK09", "MK42"]),
    ("CPL11", ["MK02", "MK09", "MK16", "MK42"]),
    ("CPL12", ["MK10", "MK40", "MK43", "MK44"]),
    ("CPL13", ["MK03", "MK36", "MK40", "MK41", "MK43", "MK44", "MK45", "MK46"]),
    ("CPL14", ["MK40", "MK43", "MK44"]),
]


def seed_cpl_mk_matrix():
    """Seed mapping CPL ke MK dari Sheet 9."""
    cpl_map = _build_map(CPLProdi, "kode")
    mk_map = _build_map(MataKuliah, "kode")

    for cpl_kode, mk_list in CPL_MK_DATA:
        cpl_id = cpl_map.get(cpl_kode)
        if cpl_id is None:
            continue
        for mk_kode in mk_list:
            mk_id = mk_map.get(mk_kode)
            if mk_id is None:
                continue
            state.db.execute(
                mapping_cpl_mk.insert().values(
                    cpl_id=cpl_id, mk_id=mk_id
                )
            )
    state.db.flush()
