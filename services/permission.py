"""
Permission resolver menggunakan dispatch table.
Tidak ada if-else bertingkat. Penambahan role cukup menambah entry di dictionary.
"""

ROLE_ACTIONS = {
    "admin_universitas": {
        "scope": "universitas",
        "allowed": {
            "view_all",
            "view_report",
            "manage_users",
        },
    },
    "dekan": {
        "scope": "fakultas",
        "allowed": {
            "view_fakultas",
            "view_report",
        },
    },
    "kaprodi": {
        "scope": "prodi",
        "allowed": {
            "view_all",
            "manage_master",
            "manage_periode",
            "manage_matrix",
            "manage_rps",
            "manage_penilaian",
            "manage_bobot",
            "lock_periode",
            "view_report",
            "manage_users",
            "input_nilai",
            "upload_bukti",
        },
    },
    "dosen": {
        "scope": "mk_assigned",
        "allowed": {
            "view_mk",
            "manage_rps",
            "input_nilai",
            "view_report_mk",
        },
    },
    "mahasiswa": {
        "scope": "self",
        "allowed": {
            "view_report_self",
        },
    },
}


def check_permission(role, action):
    """
    Memeriksa apakah role tertentu memiliki akses ke action.
    Return: True/False.
    """
    entry = ROLE_ACTIONS.get(role)
    if entry is None:
        return False
    return action in entry["allowed"]


def get_scope(role):
    """Mengambil scope akses untuk role tertentu."""
    entry = ROLE_ACTIONS.get(role)
    if entry is None:
        return None
    return entry["scope"]


def get_allowed_actions(role):
    """Mengambil seluruh action yang diizinkan untuk role."""
    entry = ROLE_ACTIONS.get(role)
    if entry is None:
        return set()
    return entry["allowed"]


def get_all_roles():
    """Mengambil seluruh role yang terdaftar."""
    return list(ROLE_ACTIONS.keys())
