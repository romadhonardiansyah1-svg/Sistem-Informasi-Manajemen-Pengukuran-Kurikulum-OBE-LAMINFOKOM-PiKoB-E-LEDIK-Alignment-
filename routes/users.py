"""
Route manajemen pengguna (khusus Kaprodi / Admin: action manage_users).
Membuat & mengelola akun dosen, tim kurikulum, dan mahasiswa.
password_hash tidak pernah dikembalikan ke client.
"""

from flask import request

import config
import state
from models.user import User, Mahasiswa
from services.auth_service import hash_password
from utils.response import success, created, not_found, error


def _user_public(u):
    return {
        "id": u.id,
        "username": u.username,
        "nama": u.nama,
        "email": u.email,
        "role": u.role,
        "prodi_id": u.prodi_id,
        "fakultas_id": u.fakultas_id,
    }


def list_users():
    """GET /api/users?role=..."""
    query = state.db.query(User)
    role = request.args.get("role")
    if role:
        query = query.filter_by(role=role)
    items = query.order_by(User.role, User.username).all()
    return success(data=[_user_public(u) for u in items])


def create_user():
    """POST /api/users"""
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or username
    role = data.get("role")

    if not username or not role:
        return error("Username dan role wajib diisi.")
    if role not in config.ROLES:
        return error("Role tidak dikenal.")
    if state.db.query(User).filter_by(username=username).first():
        return error("Username sudah digunakan.")

    user = User(
        username=username,
        password_hash=hash_password(password),
        nama=data.get("nama") or username,
        email=data.get("email"),
        role=role,
        prodi_id=data.get("prodi_id"),
        fakultas_id=data.get("fakultas_id"),
    )
    state.db.add(user)
    state.db.flush()

    # Jika mahasiswa, buat record Mahasiswa tertaut agar laporan self bekerja.
    if role == "mahasiswa":
        existing = state.db.query(Mahasiswa).filter_by(nim=username).first()
        if existing is None:
            state.db.add(Mahasiswa(
                user_id=user.id,
                nim=username,
                nama=user.nama,
                angkatan=int(data.get("angkatan") or 0),
                prodi_id=data.get("prodi_id") or 1,
            ))

    state.db.commit()
    return created(data=_user_public(user))


def update_user(record_id):
    """PUT /api/users/<id>"""
    user = state.db.query(User).get(record_id)
    if user is None:
        return not_found()

    data = request.get_json(silent=True) or {}
    for field in ("nama", "email", "prodi_id", "fakultas_id"):
        if data.get(field) is not None:
            setattr(user, field, data[field])
    if data.get("role") in config.ROLES:
        user.role = data["role"]

    state.db.commit()
    return success(data=_user_public(user), message="Pengguna diperbarui")


def reset_password(record_id):
    """POST /api/users/<id>/reset-password"""
    user = state.db.query(User).get(record_id)
    if user is None:
        return not_found()

    data = request.get_json(silent=True) or {}
    new_password = data.get("password") or user.username
    user.password_hash = hash_password(new_password)
    state.db.commit()
    return success(message="Password direset.")


def delete_user(record_id):
    """DELETE /api/users/<id>"""
    user = state.db.query(User).get(record_id)
    if user is None:
        return not_found()
    if user.username == "admin":
        return error("Akun admin tidak dapat dihapus.")

    # Lepas tautan mahasiswa bila ada.
    mhs = state.db.query(Mahasiswa).filter_by(user_id=user.id).first()
    if mhs is not None:
        mhs.user_id = None

    state.db.delete(user)
    state.db.commit()
    return success(message="Pengguna dihapus.")


ROUTE_DEFINITIONS = [
    ("GET", "/api/users", list_users, "manage_users"),
    ("POST", "/api/users", create_user, "manage_users"),
    ("PUT", "/api/users/<int:record_id>", update_user, "manage_users"),
    ("POST", "/api/users/<int:record_id>/reset-password", reset_password, "manage_users"),
    ("DELETE", "/api/users/<int:record_id>", delete_user, "manage_users"),
]
