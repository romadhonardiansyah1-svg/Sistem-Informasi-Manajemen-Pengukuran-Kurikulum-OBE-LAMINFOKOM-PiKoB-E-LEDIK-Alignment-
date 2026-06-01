"""
Standarisasi format JSON response.
Semua endpoint menggunakan format yang konsisten.
"""

from flask import jsonify


def success(data=None, message="Berhasil", status=200):
    """Response sukses."""
    body = {"status": "success", "message": message}
    if data is not None:
        body["data"] = data
    return jsonify(body), status


def created(data=None, message="Data berhasil dibuat"):
    """Response untuk resource yang baru dibuat."""
    return success(data=data, message=message, status=201)


def error(message="Terjadi kesalahan", status=400, details=None):
    """Response error."""
    body = {"status": "error", "message": message}
    if details is not None:
        body["details"] = details
    return jsonify(body), status


def not_found(message="Data tidak ditemukan"):
    """Response 404."""
    return error(message=message, status=404)


def forbidden(message="Akses ditolak"):
    """Response 403."""
    return error(message=message, status=403)


def paginated(items, total, page, page_size):
    """Response dengan informasi pagination."""
    body = {
        "status": "success",
        "data": items,
        "pagination": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        },
    }
    return jsonify(body), 200
