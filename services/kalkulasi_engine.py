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
    Menghitung skor CPL (0-100) untuk satu mahasiswa.

    Robust & tidak bergantung pada mapping_cpl_mk (yang bisa rusak/derivatif):
    skor CPL = rata-rata skor seluruh CPMK milik CPL ini (CPMK.cpl_id == cpl_id),
    di mana skor tiap CPMK = rata-rata skor_total nilai mahasiswa untuk CPMK
    tersebut (bisa dinilai di lebih dari satu MK).
    """
    cpmks = state.db.query(CPMK).filter_by(cpl_id=cpl_id).all()

    cpmk_scores = []
    detail = []
    for cpmk in cpmks:
        nilai_rows = (
            state.db.query(NilaiMahasiswa)
            .filter_by(mahasiswa_id=mahasiswa_id, cpmk_id=cpmk.id)
            .all()
        )
        if not nilai_rows:
            continue
        avg = sum((n.skor_total or 0) for n in nilai_rows) / len(nilai_rows)
        cpmk_scores.append(avg)
        detail.append({"cpmk_id": cpmk.id, "skor": round(avg, 2)})

    normalized = (sum(cpmk_scores) / len(cpmk_scores)) if cpmk_scores else 0
    grade = resolve_grade(normalized)

    return {
        "mahasiswa_id": mahasiswa_id,
        "cpl_id": cpl_id,
        "skor_raw": round(sum(cpmk_scores), 2),
        "skor_max": len(cpmk_scores) * 100,
        "skor_normalized": round(normalized, 2),
        "grade": grade,
        "detail_cpmk": detail,
    }


def hitung_seluruh_mahasiswa(mahasiswa_id):
    """
    Pipeline lengkap untuk satu mahasiswa.
    Return: seluruh skor CPL + grade.
    CPL dibatasi pada periode AKTIF agar tidak mencampur antar-periode
    (konsisten dengan laporan agregat).
    """
    from models.period import PeriodeKurikulum

    aktif = (
        state.db.query(PeriodeKurikulum)
        .filter_by(status="aktif")
        .order_by(PeriodeKurikulum.tahun_mulai.desc())
        .first()
    )

    query = state.db.query(CPLProdi)
    if aktif is not None:
        query = query.filter_by(periode_id=aktif.id)
    cpl_list = query.order_by(CPLProdi.kode).all()

    results = []
    for cpl in cpl_list:
        result = hitung_nilai_cpl(mahasiswa_id, cpl.id)
        result["cpl_kode"] = cpl.kode
        results.append(result)

    return {
        "mahasiswa_id": mahasiswa_id,
        "cpl_scores": results,
    }
