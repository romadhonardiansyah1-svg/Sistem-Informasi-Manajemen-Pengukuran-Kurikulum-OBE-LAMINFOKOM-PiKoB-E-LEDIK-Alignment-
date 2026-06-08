"""
Route upload generik (PDF) -> Supabase Storage (atau disk lokal saat dev).
"""

from flask import request

from services import storage_service
from utils.response import success, error


def upload_file():
    """POST /api/upload (single PDF)"""
    file = request.files.get("file")
    if file is None or not file.filename:
        return error("Tidak ada file yang dikirim")

    periode_id = request.form.get("periode_id", "general")
    kategori = request.form.get("kategori", "bukti")
    folder = str(periode_id) + "/" + kategori

    try:
        meta = storage_service.save_pdf(file, folder)
    except ValueError as e:
        return error(str(e))

    return success(
        data={
            "filename": meta["filename"],
            "storage_key": meta["storage_key"],
            "storage_backend": meta["storage_backend"],
            "ukuran": meta["ukuran"],
        },
        message="File berhasil diunggah",
    )


ROUTE_DEFINITIONS = [
    ("POST", "/api/upload", upload_file, "manage_dokumen"),
]
