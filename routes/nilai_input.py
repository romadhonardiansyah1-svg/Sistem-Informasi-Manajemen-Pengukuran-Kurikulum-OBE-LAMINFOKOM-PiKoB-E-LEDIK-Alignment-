"""
Route input nilai oleh dosen.
"""

from flask import request

import state
from models.nilai import NilaiMahasiswa
from models.penilaian import BobotPenilaian
from utils.response import success, created, not_found


_SCORE_FIELDS = (
    "skor_partisipasi", "skor_observasi", "skor_unjuk_kerja",
    "skor_uts", "skor_uas", "skor_tes_lisan",
)


def _compute_skor_total(rec):
    """
    Hitung skor_total (0-100) dari komponen teknik menggunakan BobotPenilaian
    (Tabel 18) untuk (mk_id, cpmk_id). Tidak mempercayai skor_total dari client
    agar konsisten dengan pipeline kalkulasi. Fallback: rata-rata komponen.
    """
    part = float(rec.get("skor_partisipasi", 0) or 0)
    obs = float(rec.get("skor_observasi", 0) or 0)
    unjuk = float(rec.get("skor_unjuk_kerja", 0) or 0)
    uts = float(rec.get("skor_uts", 0) or 0)
    uas = float(rec.get("skor_uas", 0) or 0)
    lisan = float(rec.get("skor_tes_lisan", 0) or 0)

    bp = (
        state.db.query(BobotPenilaian)
        .filter_by(mk_id=rec.get("mk_id"), cpmk_id=rec.get("cpmk_id"))
        .first()
    )
    if bp is not None and (bp.total or 0) > 0:
        total = (
            part * (bp.partisipasi_pct or 0)
            + obs * (bp.observasi_pct or 0)
            + unjuk * (bp.unjuk_kerja_pct or 0)
            + uts * (bp.uts_pct or 0)
            + uas * (bp.uas_pct or 0)
            + lisan * (bp.tes_lisan_pct or 0)
        ) / float(bp.total)
    else:
        vals = [part, obs, unjuk, uts, uas, lisan]
        total = sum(vals) / len(vals)
    return round(total, 2)


def list_nilai():
    """GET /api/nilai"""
    mk_id = request.args.get("mk_id", type=int)
    mahasiswa_id = request.args.get("mahasiswa_id", type=int)

    query = state.db.query(NilaiMahasiswa)
    if mk_id:
        query = query.filter_by(mk_id=mk_id)
    if mahasiswa_id:
        query = query.filter_by(mahasiswa_id=mahasiswa_id)

    items = query.all()
    return success(data=[i.to_dict() for i in items])


def save_nilai():
    """POST /api/nilai"""
    data = request.get_json(silent=True)
    records = data.get("records", [])

    for rec in records:
        existing = (
            state.db.query(NilaiMahasiswa)
            .filter_by(
                mahasiswa_id=rec["mahasiswa_id"],
                mk_id=rec["mk_id"],
                cpmk_id=rec["cpmk_id"],
            )
            .first()
        )

        # skor_total dihitung server-side dari komponen x BobotPenilaian.
        skor_total = _compute_skor_total(rec)

        if existing:
            for field in _SCORE_FIELDS:
                value = rec.get(field)
                if value is not None:
                    setattr(existing, field, value)
            existing.skor_total = skor_total
        else:
            nilai = NilaiMahasiswa(
                mahasiswa_id=rec["mahasiswa_id"],
                mk_id=rec["mk_id"],
                cpmk_id=rec["cpmk_id"],
                semester_aktif=rec.get("semester_aktif"),
                skor_partisipasi=rec.get("skor_partisipasi", 0),
                skor_observasi=rec.get("skor_observasi", 0),
                skor_unjuk_kerja=rec.get("skor_unjuk_kerja", 0),
                skor_uts=rec.get("skor_uts", 0),
                skor_uas=rec.get("skor_uas", 0),
                skor_tes_lisan=rec.get("skor_tes_lisan", 0),
                skor_total=skor_total,
            )
            state.db.add(nilai)

    state.db.commit()
    return created(message="Nilai disimpan")


ROUTE_DEFINITIONS = [
    ("GET", "/api/nilai", list_nilai, "input_nilai"),
    ("POST", "/api/nilai", save_nilai, "input_nilai"),
]
