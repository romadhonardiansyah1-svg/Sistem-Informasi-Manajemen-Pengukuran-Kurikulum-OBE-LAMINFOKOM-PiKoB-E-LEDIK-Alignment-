"""
Route input nilai oleh dosen.
"""

from flask import request

import state
from models.nilai import NilaiMahasiswa
from utils.response import success, created, not_found


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

        score_fields = (
            "skor_partisipasi", "skor_observasi", "skor_unjuk_kerja",
            "skor_uts", "skor_uas", "skor_tes_lisan",
        )

        if existing:
            for field in score_fields:
                value = rec.get(field)
                if value is not None:
                    setattr(existing, field, value)
            existing.skor_total = rec.get("skor_total", 0)
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
                skor_total=rec.get("skor_total", 0),
            )
            state.db.add(nilai)

    state.db.commit()
    return created(message="Nilai disimpan")


ROUTE_DEFINITIONS = [
    ("GET", "/api/nilai", list_nilai, "input_nilai"),
    ("POST", "/api/nilai", save_nilai, "input_nilai"),
]
