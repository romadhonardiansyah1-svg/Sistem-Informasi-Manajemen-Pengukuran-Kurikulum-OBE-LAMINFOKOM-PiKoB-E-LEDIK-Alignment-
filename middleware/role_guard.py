"""
Decorator otorisasi berbasis role.
Bila config.OPEN_ACCESS True, cukup butuh login (semua action diizinkan).
"""

from functools import wraps
from flask import jsonify

import config
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

            # MODE OPEN ACCESS: semua user login boleh akses semua fitur.
            if getattr(config, "OPEN_ACCESS", False):
                return handler(*args, **kwargs)

            if not check_permission(user.role, action):
                return jsonify({
                    "error": "Akses ditolak",
                    "required_action": action,
                }), 403

            return handler(*args, **kwargs)

        return wrapper
    return decorator
