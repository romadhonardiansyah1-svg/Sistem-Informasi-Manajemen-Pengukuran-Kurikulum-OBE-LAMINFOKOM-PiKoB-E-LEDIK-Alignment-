"""
Route autentikasi: login, logout, info session.
"""

from flask import request, session, jsonify

from services.auth_service import authenticate
import state
from utils.response import success, error


def login():
    """POST /api/auth/login"""
    try:
        data = request.get_json(silent=True)
        if data is None:
            return error("Request body kosong"), 400

        username = data.get("username", "")
        password = data.get("password", "")

        user = authenticate(username, password)
        if user is None:
            return error("Username atau password salah"), 401

        session["user_id"] = user["id"]
        session["role"] = user["role"]

        return success(data=user, message="Login berhasil")
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        return {
            "status": "error",
            "message": f"Server Error:\n{tb}"
        }, 500



def logout():
    """POST /api/auth/logout"""
    session.clear()
    state.current_user = None
    return success(message="Logout berhasil")


def session_info():
    """GET /api/auth/session"""
    user_id = session.get("user_id")
    if user_id is None:
        return error("Belum login", status=401)

    from models.user import User
    user = state.db.query(User).get(user_id)
    if user is None:
        session.clear()
        return error("Sesi tidak valid", status=401)

    return success(data=user.to_dict())


ROUTE_DEFINITIONS = [
    ("POST", "/api/auth/login", login, None),
    ("POST", "/api/auth/logout", logout, None),
    ("GET", "/api/auth/session", session_info, None),
]
