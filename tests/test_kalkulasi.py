"""
Unit test kalkulasi formulas.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.kalkulasi_formulas import (
    weighted_score,
    aggregate_cpmk_to_mk,
    normalize_cpl_score,
    resolve_grade,
    pemenuhan_threshold,
    calculate_weighted_total,
)


def test_weighted_score():
    assert weighted_score(75, 40) == 30.0
    assert weighted_score(100, 100) == 100.0
    assert weighted_score(0, 50) == 0.0
    assert weighted_score(83, 60) == 49.8
    print("test_weighted_score: OK")


def test_aggregate_cpmk_to_mk():
    pairs = [(75, 40), (83, 60)]
    result = aggregate_cpmk_to_mk(pairs)
    assert abs(result - 79.8) < 0.01
    print("test_aggregate_cpmk_to_mk: OK")


def test_normalize_cpl_score():
    assert normalize_cpl_score(176, 220) == 80.0
    assert normalize_cpl_score(0, 100) == 0
    assert normalize_cpl_score(100, 0) == 0
    print("test_normalize_cpl_score: OK")


def test_resolve_grade():
    assert resolve_grade(85) == "Sangat Kompeten"
    assert resolve_grade(70) == "Kompeten"
    assert resolve_grade(50) == "Cukup Kompeten"
    assert resolve_grade(30) == "Kurang Kompeten"
    assert resolve_grade(10) == "Tidak Kompeten"
    print("test_resolve_grade: OK")


def test_pemenuhan_threshold():
    assert pemenuhan_threshold(75) is True
    assert pemenuhan_threshold(60) is False
    assert pemenuhan_threshold(70) is True
    print("test_pemenuhan_threshold: OK")


def test_calculate_weighted_total():
    scores = {"partisipasi": 80, "observasi": 70}
    bobot = {"partisipasi": 40, "observasi": 60}
    result = calculate_weighted_total(scores, bobot)
    assert result == 74.0
    print("test_calculate_weighted_total: OK")


if __name__ == "__main__":
    test_weighted_score()
    test_aggregate_cpmk_to_mk()
    test_normalize_cpl_score()
    test_resolve_grade()
    test_pemenuhan_threshold()
    test_calculate_weighted_total()
    print("\nSemua test kalkulasi PASSED.")
