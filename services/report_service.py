"""
Agregasi data untuk laporan CPL.
"""

import state
from models.cpl import CPLProdi
from models.user import Mahasiswa
from services.kalkulasi_engine import hitung_seluruh_mahasiswa
from services.kalkulasi_formulas import resolve_grade, pemenuhan_threshold


def get_cpl_report_mahasiswa(mahasiswa_id):
    """
    Laporan CPL untuk satu mahasiswa.
    Return: skor per CPL + grade + spider chart data.
    """
    result = hitung_seluruh_mahasiswa(mahasiswa_id)

    spider_data = []
    for cpl_score in result["cpl_scores"]:
        spider_data.append({
            "label": cpl_score["cpl_kode"],
            "value": cpl_score["skor_normalized"],
            "grade": cpl_score["grade"],
            "lulus": pemenuhan_threshold(cpl_score["skor_normalized"]),
        })

    result["spider_chart"] = spider_data
    return result


def get_cpl_report_agregat(angkatan, periode_id):
    """
    Laporan CPL agregat per angkatan.
    Menghitung persentase mahasiswa yang lulus per CPL.
    """
    mahasiswa_list = (
        state.db.query(Mahasiswa)
        .filter_by(angkatan=angkatan)
        .all()
    )

    cpl_list = (
        state.db.query(CPLProdi)
        .filter_by(periode_id=periode_id)
        .order_by(CPLProdi.kode)
        .all()
    )

    total_mahasiswa = len(mahasiswa_list)
    cpl_stats = []

    for cpl in cpl_list:
        lulus_count = 0
        scores = []

        for mhs in mahasiswa_list:
            from services.kalkulasi_engine import hitung_nilai_cpl
            result = hitung_nilai_cpl(mhs.id, cpl.id)
            normalized = result["skor_normalized"]
            scores.append(normalized)
            if pemenuhan_threshold(normalized):
                lulus_count += 1

        avg_score = sum(scores) / len(scores) if scores else 0
        pct_lulus = (lulus_count / total_mahasiswa * 100) if total_mahasiswa > 0 else 0

        cpl_stats.append({
            "cpl_kode": cpl.kode,
            "cpl_deskripsi": cpl.deskripsi,
            "rata_rata": round(avg_score, 2),
            "persen_lulus": round(pct_lulus, 2),
            "jumlah_lulus": lulus_count,
            "total_mahasiswa": total_mahasiswa,
            "grade": resolve_grade(avg_score),
        })

    return {
        "angkatan": angkatan,
        "periode_id": periode_id,
        "cpl_stats": cpl_stats,
    }
