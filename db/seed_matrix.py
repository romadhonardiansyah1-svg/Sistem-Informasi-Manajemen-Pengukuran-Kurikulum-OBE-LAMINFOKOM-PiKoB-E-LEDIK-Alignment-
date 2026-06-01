"""
Seed data matriks pemetaan dari Sheet 5 (CPL-PL), Sheet 7 (CPL-BK), Sheet 8 (BK-MK).
Menggunakan Table objects langsung dari models/mapping.py.
"""

import state
from models.mapping import mapping_cpl_pl, mapping_cpl_bk, mapping_bk_mk
from models.cpl import CPLProdi
from models.profil_lulusan import ProfilLulusan
from models.bahan_kajian import BahanKajian
from models.mata_kuliah import MataKuliah


def _get_id_map(model, field):
    """Buat map kode -> id dari model."""
    result = {}
    rows = state.db.query(model).all()
    for row in rows:
        result[getattr(row, field)] = row.id
    return result


def seed_cpl_pl_matrix():
    """Seed matriks CPL-PL dari Sheet 5."""
    cpl_map = _get_id_map(CPLProdi, "kode")
    pl_map = _get_id_map(ProfilLulusan, "kode")

    mappings = [
        ("CPL01", ["PL1", "PL2", "PL3", "PL5"]),
        ("CPL02", ["PL1", "PL3"]),
        ("CPL03", ["PL1"]),
        ("CPL04", ["PL1"]),
        ("CPL05", ["PL1", "PL2", "PL3", "PL4", "PL5"]),
        ("CPL06", ["PL2"]),
        ("CPL07", ["PL1"]),
        ("CPL08", ["PL3"]),
        ("CPL09", ["PL2"]),
        ("CPL10", ["PL4"]),
        ("CPL11", ["PL4"]),
        ("CPL12", ["PL5"]),
        ("CPL13", ["PL5"]),
        ("CPL14", ["PL5"]),
    ]

    for cpl_kode, pl_list in mappings:
        cpl_id = cpl_map.get(cpl_kode)
        if not cpl_id:
            continue
        for pl_kode in pl_list:
            pl_id = pl_map.get(pl_kode)
            if not pl_id:
                continue
            state.db.execute(
                mapping_cpl_pl.insert().values(cpl_id=cpl_id, pl_id=pl_id)
            )
    state.db.flush()


def seed_cpl_bk_matrix():
    """Seed matriks CPL-BK dari Sheet 7."""
    cpl_map = _get_id_map(CPLProdi, "kode")
    bk_map = _get_id_map(BahanKajian, "kode")

    mappings = [
        ("BK01", ["CPL01", "CPL02", "CPL05", "CPL07", "CPL09"]),
        ("BK02", ["CPL02", "CPL08"]),
        ("BK03", ["CPL04"]),
        ("BK04", ["CPL07"]),
        ("BK05", ["CPL03"]),
        ("BK06", ["CPL06"]),
        ("BK07", ["CPL03"]),
        ("BK08", ["CPL04", "CPL06"]),
        ("BK09", ["CPL05", "CPL10", "CPL11"]),
        ("BK10", ["CPL02", "CPL07", "CPL12", "CPL13", "CPL14"]),
        ("BK11", ["CPL02", "CPL08"]),
        ("BK12", ["CPL08"]),
        ("BK13", ["CPL05", "CPL10", "CPL11", "CPL12", "CPL13", "CPL14"]),
        ("BK14", ["CPL09"]),
        ("BK15", ["CPL04", "CPL06"]),
        ("BK16", ["CPL03"]),
        ("BK17", ["CPL03"]),
        ("BK18", ["CPL08"]),
        ("BK19", ["CPL03"]),
        ("BK20", ["CPL03"]),
        ("BK21", ["CPL03"]),
    ]

    for bk_kode, cpl_list in mappings:
        bk_id = bk_map.get(bk_kode)
        if not bk_id:
            continue
        for cpl_kode in cpl_list:
            cpl_id = cpl_map.get(cpl_kode)
            if not cpl_id:
                continue
            state.db.execute(
                mapping_cpl_bk.insert().values(cpl_id=cpl_id, bk_id=bk_id)
            )
    state.db.flush()


def seed_bk_mk_matrix():
    """Seed matriks BK-MK dari Sheet 8."""
    bk_map = _get_id_map(BahanKajian, "kode")
    mk_map = _get_id_map(MataKuliah, "kode")

    mappings = [
        ("BK01", ["MK04", "MK06"]),
        ("BK02", ["MK11", "MK21", "MK24", "MK32"]),
        ("BK03", ["MK06", "MK13", "MK27", "MK48", "MK51"]),
        ("BK04", ["MK23"]),
        ("BK05", ["MK19", "MK20"]),
        ("BK06", ["MK14", "MK30", "MK33", "MK37", "MK38", "MK52", "MK53", "MK54", "MK55", "MK56"]),
        ("BK07", ["MK05", "MK12", "MK18", "MK22", "MK29", "MK47", "MK49"]),
        ("BK08", ["MK31", "MK48"]),
        ("BK09", ["MK39", "MK40", "MK43", "MK46", "MK01", "MK02", "MK09"]),
        ("BK10", ["MK34", "MK40", "MK43", "MK44", "MK45"]),
        ("BK11", ["MK07", "MK10", "MK11", "MK24", "MK28", "MK35"]),
        ("BK12", ["MK24", "MK32", "MK57", "MK59", "MK60", "MK61"]),
        ("BK13", ["MK01", "MK02", "MK08", "MK09", "MK42", "MK03", "MK36"]),
        ("BK14", ["MK15", "MK25", "MK65", "MK66"]),
        ("BK15", ["MK50", "MK25"]),
        ("BK16", ["MK20"]),
        ("BK17", ["MK16", "MK18", "MK26", "MK62", "MK63", "MK64"]),
        ("BK18", ["MK32", "MK58"]),
        ("BK19", ["MK18"]),
        ("BK20", ["MK22"]),
        ("BK21", ["MK47"]),
    ]

    for bk_kode, mk_list in mappings:
        bk_id = bk_map.get(bk_kode)
        if not bk_id:
            continue
        for mk_kode in mk_list:
            mk_id = mk_map.get(mk_kode)
            if not mk_id:
                continue
            state.db.execute(
                mapping_bk_mk.insert().values(bk_id=bk_id, mk_id=mk_id)
            )
    state.db.flush()
