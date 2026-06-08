"""
Route dashboard: halaman utama per role.
"""

import state
from utils.response import success


def get_dashboard():
    """GET /api/dashboard"""
    user = state.current_user
    data = {
        "user": user.to_dict(),
        "role": user.role,
    }
    return success(data=data)


ROUTE_DEFINITIONS = [
    ("GET", "/api/dashboard", get_dashboard, "view_kurikulum"),
]
