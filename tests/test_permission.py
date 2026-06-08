"""
Unit test permission resolver.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.permission import (
    check_permission,
    get_scope,
    get_allowed_actions,
    get_all_roles,
)


def test_kaprodi_permissions():
    assert check_permission("kaprodi", "manage_master") is True
    assert check_permission("kaprodi", "manage_matrix") is True
    assert check_permission("kaprodi", "view_report") is True
    assert check_permission("kaprodi", "unknown_action") is False
    print("test_kaprodi_permissions: OK")


def test_dosen_permissions():
    assert check_permission("dosen", "input_nilai") is True
    assert check_permission("dosen", "manage_master") is False
    assert check_permission("dosen", "view_kurikulum") is True
    assert check_permission("dosen", "manage_rps") is True
    print("test_dosen_permissions: OK")


def test_tim_kurikulum_permissions():
    # Tim kurikulum: hanya master data & matriks.
    assert check_permission("tim_kurikulum", "manage_master") is True
    assert check_permission("tim_kurikulum", "manage_matrix") is True
    assert check_permission("tim_kurikulum", "input_nilai") is False
    assert check_permission("tim_kurikulum", "manage_periode") is False
    assert check_permission("tim_kurikulum", "manage_users") is False
    print("test_tim_kurikulum_permissions: OK")


def test_mahasiswa_permissions():
    assert check_permission("mahasiswa", "view_report_self") is True
    assert check_permission("mahasiswa", "manage_master") is False
    assert check_permission("mahasiswa", "input_nilai") is False
    assert check_permission("mahasiswa", "view_kurikulum") is False
    print("test_mahasiswa_permissions: OK")


def test_admin_permissions():
    assert check_permission("admin_universitas", "view_kurikulum") is True
    assert check_permission("admin_universitas", "manage_users") is True
    assert check_permission("admin_universitas", "manage_master") is False
    print("test_admin_permissions: OK")


def test_unknown_role():
    assert check_permission("nonexistent", "view_kurikulum") is False
    assert get_scope("nonexistent") is None
    assert get_allowed_actions("nonexistent") == []
    print("test_unknown_role: OK")


def test_get_scope():
    assert get_scope("kaprodi") == "prodi"
    assert get_scope("tim_kurikulum") == "prodi"
    assert get_scope("dosen") == "mk_assigned"
    assert get_scope("mahasiswa") == "self"
    print("test_get_scope: OK")


def test_get_all_roles():
    roles = get_all_roles()
    assert "kaprodi" in roles
    assert "tim_kurikulum" in roles
    assert "dosen" in roles
    assert "mahasiswa" in roles
    assert len(roles) == 6
    print("test_get_all_roles: OK")


if __name__ == "__main__":
    test_kaprodi_permissions()
    test_dosen_permissions()
    test_tim_kurikulum_permissions()
    test_mahasiswa_permissions()
    test_admin_permissions()
    test_unknown_role()
    test_get_scope()
    test_get_all_roles()
    print("\nSemua test permission PASSED.")
