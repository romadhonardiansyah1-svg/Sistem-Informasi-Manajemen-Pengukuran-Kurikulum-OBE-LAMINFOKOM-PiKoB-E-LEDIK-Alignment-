"""
Agregasi data untuk laporan CPL.
"""

import config
import state
from models.cpl import CPLProdi
from models.user import Mahasiswa
from services.kalkulasi_engine import hitung_seluruh_mahasiswa
from services.kalkulasi_formulas import resolve_grade, pemenuhan_threshold


def get_cpl_report_mahasiswa(mahasiswa_id):
    """
    Laporan CPL untuk satu mahasiswa.
    Return: skor per CPL + grade + spider chart data + ringkasan ketercapaian.
    """
    result = hitung_seluruh_mahasiswa(mahasiswa_id)

    cpl_map = {c.id: c for c in state.db.query(CPLProdi).all()}

    spider_data = []
    total = 0.0
    lulus = 0
    for cpl_score in result["cpl_scores"]:
        cpl = cpl_map.get(cpl_score["cpl_id"])
        nilai = cpl_score["skor_normalized"]
        is_lulus = pemenuhan_threshold(nilai)
        spider_data.append({
            "cpl_id": cpl_score["cpl_id"],
            "label": cpl_score["cpl_kode"],
            "deskripsi": cpl.deskripsi if cpl else "",
            "value": nilai,
            "grade": cpl_score["grade"],
            "lulus": is_lulus,
        })
        total += nilai
        if is_lulus:
            lulus += 1

    n = len(spider_data)
    result["spider_chart"] = spider_data
    result["ringkasan"] = {
        "rata_rata": round(total / n, 2) if n else 0,
        "jumlah_cpl": n,
        "jumlah_lulus": lulus,
        "persen_lulus": round(lulus / n * 100, 2) if n else 0,
        "threshold": config.SKOR_PEMENUHAN_CPL_MINIMAL,
    }
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
