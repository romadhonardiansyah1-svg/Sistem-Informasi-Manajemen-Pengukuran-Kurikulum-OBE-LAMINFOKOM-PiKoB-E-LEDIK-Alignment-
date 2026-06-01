"""
Logika autentikasi: hashing, verifikasi, session management.
"""

from werkzeug.security import generate_password_hash, check_password_hash

import state


def hash_password(plain_text):
    """Menghasilkan hash dari password plain text."""
    return generate_password_hash(plain_text, method="pbkdf2:sha256")


def verify_password(plain_text, hashed):
    """Verifikasi password plain text terhadap hash."""
    return check_password_hash(hashed, plain_text)


def authenticate(username, password):
    """
    Mencari user berdasarkan username dan memverifikasi password.
    Return: user dict atau None.
    """
    from models.user import User

    user = state.db.query(User).filter_by(username=username).first()
    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user.to_dict()


def create_user(username, password, nama, email, role, prodi_id=None, fakultas_id=None):
    """Membuat user baru dengan password ter-hash."""
    from models.user import User

    user = User(
        username=username,
        password_hash=hash_password(password),
        nama=nama,
        email=email,
        role=role,
        prodi_id=prodi_id,
        fakultas_id=fakultas_id,
    )
    state.db.add(user)
    state.db.commit()
    return user.to_dict()
