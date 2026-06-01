"""
Route upload bukti fisik (PDF).
"""

import os
from flask import request, send_from_directory

import config
import state
from utils.response import success, error


def upload_file():
    """POST /api/upload"""
    file = request.files.get("file")
    if file is None:
        return error("Tidak ada file yang dikirim")

    filename = file.filename
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in config.ALLOWED_EXTENSIONS:
        return error("Format file tidak diizinkan. Hanya PDF.")

    periode_id = request.form.get("periode_id", "general")
    kategori = request.form.get("kategori", "bukti")

    upload_path = os.path.join(config.UPLOAD_DIR, str(periode_id), kategori)
    os.makedirs(upload_path, exist_ok=True)

    file_path = os.path.join(upload_path, filename)
    file.save(file_path)

    return success(
        data={"filename": filename, "path": file_path},
        message="File berhasil diunggah",
    )


def get_upload(periode_id, kategori, filename):
    """GET /uploads/<periode_id>/<kategori>/<filename>"""
    upload_path = os.path.join(config.UPLOAD_DIR, str(periode_id), kategori)
    return send_from_directory(upload_path, filename)


ROUTE_DEFINITIONS = [
    ("POST", "/api/upload", upload_file, "upload_bukti"),
    ("GET", "/uploads/<periode_id>/<kategori>/<filename>", get_upload, "view_all"),
]
