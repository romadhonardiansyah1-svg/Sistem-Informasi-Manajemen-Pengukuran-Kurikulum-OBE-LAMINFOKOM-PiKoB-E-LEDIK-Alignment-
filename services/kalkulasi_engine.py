"""
Mesin kalkulasi berjenjang.
Pipeline: Nilai -> Sub-CPMK -> CPMK -> MK -> CPL -> PL.
Mengacu pada Tabel 18-20 dan contoh di halaman 68-69.
"""

import state
from models.nilai import NilaiMahasiswa
from models.penilaian import BobotPenilaian, TahapPenilaian
from models.cpmk import CPMK
from models.cpl import CPLProdi
from models.mapping import mapping_cpl_pl, mapping_cpl_mk
from services.kalkulasi_formulas import (
    weighted_score, aggregate_cpmk_to_mk,
    normalize_cpl_score, resolve_grade,
)


def hitung_nilai_mk(mahasiswa_id, mk_id):
    """
    Menghitung nilai akhir MK untuk satu mahasiswa.
    Mengambil semua CPMK pada MK, lalu weighted sum.
    Total bobot per MK = 100.
    """
    tahap_list = (
        state.db.query(TahapPenilaian)
        .filter_by(mk_id=mk_id)
        .all()
    )

    cpmk_scores = []
    for tahap in tahap_list:
        nilai = (
            state.db.query(NilaiMahasiswa)
            .filter_by(
                mahasiswa_id=mahasiswa_id,
                mk_id=mk_id,
                cpmk_id=tahap.cpmk_id,
            )
            .first()
        )

        skor_mentah = nilai.skor_total if nilai else 0
        cpmk_scores.append((skor_mentah, tahap.bobot))

    nilai_mk = aggregate_cpmk_to_mk(cpmk_scores)
    grade = resolve_grade(nilai_mk)

    return {
        "mahasiswa_id": mahasiswa_id,
        "mk_id": mk_id,
        "nilai_mk": round(nilai_mk, 2),
        "grade": grade,
        "detail": [
            {"cpmk_id": t.cpmk_id, "bobot": t.bobot, "skor": s}
            for t, (s, _) in zip(tahap_list, cpmk_scores)
        ],
    }


def hitung_nilai_cpl(mahasiswa_id, cpl_id):
    """
    Menghitung skor CPL untuk satu mahasiswa.
    Agregasi dari semua MK yang memiliki CPL ini.
    """
    rows = state.db.execute(
        mapping_cpl_mk.select().where(mapping_cpl_mk.c.cpl_id == cpl_id)
    ).fetchall()

    mk_ids = [r.mk_id for r in rows]
    total_raw = 0
    total_max = 0
    detail = []

    for mk_id in mk_ids:
        tahap_list = (
            state.db.query(TahapPenilaian)
            .filter_by(mk_id=mk_id, cpl_id=cpl_id)
            .all()
        )

        mk_skor = 0
        mk_max = 0
        for tahap in tahap_list:
            nilai = (
                state.db.query(NilaiMahasiswa)
                .filter_by(
                    mahasiswa_id=mahasiswa_id,
                    mk_id=mk_id,
                    cpmk_id=tahap.cpmk_id,
                )
                .first()
            )
            skor = nilai.skor_total if nilai else 0
            mk_skor += weighted_score(skor, tahap.bobot)
            mk_max += tahap.bobot

        total_raw += mk_skor
        total_max += mk_max
        detail.append({"mk_id": mk_id, "skor": round(mk_skor, 2), "max": mk_max})

    normalized = normalize_cpl_score(total_raw, total_max)
    grade = resolve_grade(normalized)

    return {
        "mahasiswa_id": mahasiswa_id,
        "cpl_id": cpl_id,
        "skor_raw": round(total_raw, 2),
        "skor_max": total_max,
        "skor_normalized": round(normalized, 2),
        "grade": grade,
        "detail_mk": detail,
    }


def hitung_seluruh_mahasiswa(mahasiswa_id):
    """
    Pipeline lengkap untuk satu mahasiswa.
    Return: seluruh skor CPL + grade.
    """
    cpl_list = state.db.query(CPLProdi).all()
    results = []

    for cpl in cpl_list:
        result = hitung_nilai_cpl(mahasiswa_id, cpl.id)
        result["cpl_kode"] = cpl.kode
        results.append(result)

    return {
        "mahasiswa_id": mahasiswa_id,
        "cpl_scores": results,
    }
