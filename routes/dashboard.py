"""
Route dashboard: halaman utama per role.
"""

import state
from utils.response import success


def get_dashboard():
    """GET /api/dashboard"""
    user = state.current_user
    # Jangan kirim objek User mentah (to_dict membawa password_hash). Pakai payload aman.
    data = {
        "user": {
            "id": user.id,
            "username": user.username,
            "nama": user.nama,
            "email": user.email,
            "role": user.role,
            "prodi_id": user.prodi_id,
            "fakultas_id": user.fakultas_id,
        },
        "role": user.role,
    }
    return success(data=data)


ROUTE_DEFINITIONS = [
    ("GET", "/api/dashboard", get_dashboard, "view_kurikulum"),
]
