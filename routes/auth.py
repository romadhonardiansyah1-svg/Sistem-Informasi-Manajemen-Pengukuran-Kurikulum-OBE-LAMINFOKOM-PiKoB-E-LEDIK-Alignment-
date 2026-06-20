"""
Route autentikasi: login, logout, info session.
"""

from flask import request, session

from services.auth_service import authenticate
import state
from utils.response import success, error


def _build_session_payload(user_dict):
    """
    Membentuk payload aman untuk frontend dari dict user:
    - buang password_hash (jangan pernah dikirim ke client)
    - sertakan allowed_actions + scope sesuai role (untuk filter menu di frontend)
    - jika OPEN_ACCESS, gabungkan SEMUA action → sidebar tampilkan semua menu
    - jika role mahasiswa, sertakan mahasiswa_id/nim/angkatan agar laporan bisa self-scoped
    """
    import config
    from services.permission import get_allowed_actions, get_scope, ROLE_ACTIONS

    role = user_dict.get("role")
    payload = {k: v for k, v in user_dict.items() if k != "password_hash"}
    payload["allowed_actions"] = get_allowed_actions(role)
    payload["scope"] = get_scope(role)

    # Mode akses terbuka: kirim semua action agar frontend tampilkan semua menu
    payload["open_access"] = getattr(config, "OPEN_ACCESS", False)
    if payload["open_access"]:
        semua = set()
        for r in ROLE_ACTIONS.values():
            semua |= set(r["allowed"])
        payload["allowed_actions"] = sorted(semua)

    if role == "mahasiswa":
        from models.user import Mahasiswa
        mhs = (
            state.db.query(Mahasiswa)
            .filter_by(user_id=user_dict.get("id"))
            .first()
        )
        if mhs is not None:
            payload["mahasiswa_id"] = mhs.id
            payload["nim"] = mhs.nim
            payload["angkatan"] = mhs.angkatan

    return payload


def login():
    """POST /api/auth/login"""
    try:
        data = request.get_json(silent=True)
        if data is None:
            return error("Request body kosong")

        username = data.get("username", "")
        password = data.get("password", "")

        user = authenticate(username, password)
        if user is None:
            return error("Username atau password salah", status=401)

        session["user_id"] = user["id"]
        session["role"] = user["role"]

        return success(data=_build_session_payload(user), message="Login berhasil")
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

    return success(data=_build_session_payload(user.to_dict()))


ROUTE_DEFINITIONS = [
    ("POST", "/api/auth/login", login, None),
    ("POST", "/api/auth/logout", logout, None),
    ("GET", "/api/auth/session", session_info, None),
]
