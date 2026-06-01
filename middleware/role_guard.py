"""
Decorator otorisasi berbasis role.
Menggunakan permission.py dispatch table, bukan if-else.
"""

from functools import wraps
from flask import jsonify

import state
from services.permission import check_permission


def require_action(action):
    """
    Decorator factory yang memeriksa apakah user memiliki
    izin untuk melakukan action tertentu.

    Pemakaian:
        @require_action("manage_master")
        def create_cpl():
            ...
    """
    def decorator(handler):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            user = state.current_user
            if user is None:
                return jsonify({"error": "Autentikasi diperlukan"}), 401

            has_access = check_permission(user.role, action)
            if not has_access:
                return jsonify({
                    "error": "Akses ditolak",
                    "required_action": action,
                }), 403

            return handler(*args, **kwargs)

        return wrapper
    return decorator
