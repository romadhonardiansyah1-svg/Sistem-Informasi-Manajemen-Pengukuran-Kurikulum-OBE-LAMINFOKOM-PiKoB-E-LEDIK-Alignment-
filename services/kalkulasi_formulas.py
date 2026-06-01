"""
Rumus-rumus kalkulasi terisolasi.
Setiap fungsi bisa di-unit-test secara independen.
Mengacu pada Buku Panduan halaman 59-69.
"""

import config


def weighted_score(nilai_mentah, bobot_persen):
    """
    Menghitung skor berbobot.
    Contoh: weighted_score(75, 40) -> 30.0
    """
    return nilai_mentah * bobot_persen / 100


def aggregate_cpmk_to_mk(cpmk_scores_with_bobot):
    """
    Agregasi skor CPMK ke nilai MK.
    Input: [(skor_mentah, bobot_persen), ...]
    Output: nilai_mk (total bobot = 100)

    Contoh dari buku (hal 68-69):
        [(75, 40), (83, 60)] -> 30 + 49.8 = 79.8
    """
    return sum(weighted_score(s, b) for s, b in cpmk_scores_with_bobot)


def aggregate_mk_to_cpl(mk_cpmk_pairs):
    """
    Agregasi skor CPMK dari berbagai MK ke satu CPL.
    Input: [(skor_cpmk, bobot_cpmk), ...]
    Output: skor_cpl (bisa > 100)

    Contoh dari Tabel 20:
        CPL01 total skor maks = 220
    """
    return sum(weighted_score(s, b) for s, b in mk_cpmk_pairs)


def normalize_cpl_score(raw_score, max_possible):
    """
    Normalisasi ke skala 0-100 untuk visualisasi.
    Contoh: normalize_cpl_score(176, 220) -> 80.0
    """
    if max_possible <= 0:
        return 0
    return (raw_score / max_possible) * 100


def resolve_grade(score):
    """
    Menentukan grade berdasarkan skor.
    Menggunakan lookup di config.RUBRIK_GRADE_RANGES.

    Contoh: resolve_grade(80) -> "Kompeten"
    """
    for (low, high), label in config.RUBRIK_GRADE_RANGES.items():
        if low <= score <= high:
            return label
    return "Tidak Terklasifikasi"


def calculate_weighted_total(scores, bobot):
    """
    Menghitung total tertimbang dari dictionary skor dan bobot.
    scores: {"partisipasi": 80, "observasi": 70, ...}
    bobot:  {"partisipasi": 20, "observasi": 30, ...}
    """
    total = 0
    for key, persen in bobot.items():
        nilai = scores.get(key, 0)
        total += weighted_score(nilai, persen)
    return total


def pemenuhan_threshold(score, threshold=None):
    """
    Mengecek apakah skor melewati threshold pemenuhan CPL.
    Default threshold dari config.SKOR_PEMENUHAN_CPL_MINIMAL.
    """
    if threshold is None:
        threshold = config.SKOR_PEMENUHAN_CPL_MINIMAL
    return score >= threshold
