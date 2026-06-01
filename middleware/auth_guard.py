"""
Decorator autentikasi. Memastikan user sudah login sebelum mengakses endpoint.
"""

from functools import wraps
from flask import session, jsonify

import state
from models.user import User


def login_required(handler):
    """
    Decorator yang memeriksa session login.
    Jika belum login, return 401.
    Jika sudah login, set state.current_user dan lanjutkan.
    """
    @wraps(handler)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if user_id is None:
            return jsonify({"error": "Autentikasi diperlukan"}), 401

        user = state.db.query(User).get(user_id)
        if user is None:
            session.clear()
            return jsonify({"error": "Sesi tidak valid"}), 401

        state.current_user = user
        return handler(*args, **kwargs)

    return wrapper
