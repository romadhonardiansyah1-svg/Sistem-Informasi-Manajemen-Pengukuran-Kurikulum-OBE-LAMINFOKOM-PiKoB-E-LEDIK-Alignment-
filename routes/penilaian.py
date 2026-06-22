"""
Route penilaian: teknik, tahap, dan bobot penilaian.
Tabel 16, 17, 18 Buku Panduan APTIKOM.
"""

from flask import request

import state
from models.penilaian import TeknikPenilaian, TahapPenilaian, BobotPenilaian
from utils.response import success, created, not_found, error
from services.lock_guard import assert_unlocked_by_mk


def _enrich(dicts):
    """Tambahkan kode CPL/MK/CPMK yang mudah dibaca ke baris penilaian."""
    from models.cpl import CPLProdi
    from models.mata_kuliah import MataKuliah
    from models.cpmk import CPMK

    cpl = {c.id: c.kode for c in state.db.query(CPLProdi).all()}
    mk = {m.id: m.kode for m in state.db.query(MataKuliah).all()}
    cpmk = {c.id: c.kode for c in state.db.query(CPMK).all()}
    for d in dicts:
        if "cpl_id" in d:
            d["cpl_kode"] = cpl.get(d["cpl_id"], "-")
        if "mk_id" in d:
            d["mk_kode"] = mk.get(d["mk_id"], "-")
        if "cpmk_id" in d:
            d["cpmk_kode"] = cpmk.get(d["cpmk_id"], "-")
    return dicts


def _guard_records_by_mk(records):
    """BUG-6: tolak penyimpanan bila periode MK terkait sedang terkunci."""
    seen = set()
    for rec in records:
        mk_id = rec.get("mk_id")
        if mk_id and mk_id not in seen:
            seen.add(mk_id)
            assert_unlocked_by_mk(mk_id)


def list_teknik_penilaian():
    """GET /api/penilaian/teknik"""
    mk_id = request.args.get("mk_id", type=int)
    query = state.db.query(TeknikPenilaian)
    if mk_id:
        query = query.filter_by(mk_id=mk_id)
    items = query.all()
    return success(data=_enrich([i.to_dict() for i in items]))


def save_teknik_penilaian():
    """POST /api/penilaian/teknik"""
    data = request.get_json(silent=True)
    records = data.get("records", [])
    try:
        _guard_records_by_mk(records)
    except ValueError as e:
        return error(str(e), status=423)
    for rec in records:
        tp = TeknikPenilaian(
            cpl_id=rec["cpl_id"],
            mk_id=rec["mk_id"],
            cpmk_id=rec["cpmk_id"],
            partisipasi=rec.get("partisipasi", False),
            observasi=rec.get("observasi", False),
            unjuk_kerja=rec.get("unjuk_kerja", False),
            tes_tulis_uts=rec.get("tes_tulis_uts", False),
            tes_tulis_uas=rec.get("tes_tulis_uas", False),
            tes_lisan=rec.get("tes_lisan", False),
        )
        state.db.add(tp)
    state.db.commit()
    return created(message="Teknik penilaian disimpan")


def list_tahap_penilaian():
    """GET /api/penilaian/tahap"""
    mk_id = request.args.get("mk_id", type=int)
    query = state.db.query(TahapPenilaian)
    if mk_id:
        query = query.filter_by(mk_id=mk_id)
    items = query.all()
    return success(data=_enrich([i.to_dict() for i in items]))


def save_tahap_penilaian():
    """POST /api/penilaian/tahap"""
    data = request.get_json(silent=True)
    records = data.get("records", [])
    try:
        _guard_records_by_mk(records)
    except ValueError as e:
        return error(str(e), status=423)
    for rec in records:
        tp = TahapPenilaian(
            cpl_id=rec["cpl_id"],
            mk_id=rec["mk_id"],
            cpmk_id=rec["cpmk_id"],
            tahap=rec.get("tahap"),
            teknik_penilaian_text=rec.get("teknik_penilaian_text"),
            instrumen=rec.get("instrumen"),
            kriteria=rec.get("kriteria"),
            bobot=rec.get("bobot", 0),
        )
        state.db.add(tp)
    state.db.commit()
    return created(message="Tahap penilaian disimpan")


def list_bobot_penilaian():
    """GET /api/penilaian/bobot"""
    mk_id = request.args.get("mk_id", type=int)
    query = state.db.query(BobotPenilaian)
    if mk_id:
        query = query.filter_by(mk_id=mk_id)
    items = query.all()
    return success(data=_enrich([i.to_dict() for i in items]))


def save_bobot_penilaian():
    """POST /api/penilaian/bobot"""
    data = request.get_json(silent=True)
    records = data.get("records", [])
    try:
        _guard_records_by_mk(records)
    except ValueError as e:
        return error(str(e), status=423)
    for rec in records:
        bp = BobotPenilaian(
            cpl_id=rec["cpl_id"],
            mk_id=rec["mk_id"],
            cpmk_id=rec["cpmk_id"],
            partisipasi_pct=rec.get("partisipasi_pct", 0),
            observasi_pct=rec.get("observasi_pct", 0),
            unjuk_kerja_pct=rec.get("unjuk_kerja_pct", 0),
            uts_pct=rec.get("uts_pct", 0),
            uas_pct=rec.get("uas_pct", 0),
            tes_lisan_pct=rec.get("tes_lisan_pct", 0),
            total=rec.get("total", 0),
        )
        state.db.add(bp)
    state.db.commit()
    return created(message="Bobot penilaian disimpan")


ROUTE_DEFINITIONS = [
    ("GET", "/api/penilaian/teknik", list_teknik_penilaian, "view_kurikulum"),
    ("POST", "/api/penilaian/teknik", save_teknik_penilaian, "manage_penilaian"),
    ("GET", "/api/penilaian/tahap", list_tahap_penilaian, "view_kurikulum"),
    ("POST", "/api/penilaian/tahap", save_tahap_penilaian, "manage_penilaian"),
    ("GET", "/api/penilaian/bobot", list_bobot_penilaian, "view_kurikulum"),
    ("POST", "/api/penilaian/bobot", save_bobot_penilaian, "manage_bobot"),
]
