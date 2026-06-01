"""
Route log peninjauan kurikulum.
CRUD log rapat + upload dokumen bukti fisik.
T-13.1b, T-13.2 Backlog Notion.
"""

import os
from datetime import date
from flask import request

import config
import state
from models.log_peninjauan import LogPeninjauan, DokumenBukti
from utils.response import success, created, not_found, error


def list_log():
    """GET /api/log-peninjauan"""
    items = (
        state.db.query(LogPeninjauan)
        .order_by(LogPeninjauan.tanggal.desc())
        .all()
    )
    data = []
    for item in items:
        d = item.to_dict()
        d["dokumen_count"] = item.dokumen_list.count()
        data.append(d)
    return success(data=data)


def create_log():
    """POST /api/log-peninjauan"""
    body = request.get_json(silent=True)
    log = LogPeninjauan(
        judul=body["judul"],
        tanggal=date.fromisoformat(body["tanggal"]),
        peserta=body.get("peserta", ""),
        catatan=body.get("catatan", ""),
        status=body.get("status", "draft"),
    )
    state.db.add(log)
    state.db.commit()
    return created(data=log.to_dict())


def get_log(record_id):
    """GET /api/log-peninjauan/<id>"""
    log = state.db.query(LogPeninjauan).get(record_id)
    if log is None:
        return not_found()

    d = log.to_dict()
    d["dokumen"] = [doc.to_dict() for doc in log.dokumen_list.all()]
    return success(data=d)


def upload_bukti(record_id):
    """POST /api/log-peninjauan/<id>/upload"""
    log = state.db.query(LogPeninjauan).get(record_id)
    if log is None:
        return not_found()

    files = request.files.getlist("files")
    if not files:
        return error("Tidak ada file yang dikirim")

    uploaded = []
    upload_dir = os.path.join(config.UPLOAD_DIR, "peninjauan", str(record_id))
    os.makedirs(upload_dir, exist_ok=True)

    for f in files:
        ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else ""
        if ext not in config.ALLOWED_EXTENSIONS:
            continue

        filepath = os.path.join(upload_dir, f.filename)
        f.save(filepath)

        doc = DokumenBukti(
            log_id=record_id,
            filename=f.filename,
            filepath=filepath,
            ukuran=os.path.getsize(filepath),
        )
        state.db.add(doc)
        uploaded.append(f.filename)

    state.db.commit()
    return created(
        data={"uploaded": uploaded, "count": len(uploaded)},
        message=str(len(uploaded)) + " file berhasil diunggah",
    )


def delete_dokumen(record_id):
    """DELETE /api/dokumen-bukti/<id>"""
    doc = state.db.query(DokumenBukti).get(record_id)
    if doc is None:
        return not_found()

    if os.path.exists(doc.filepath):
        os.remove(doc.filepath)

    state.db.delete(doc)
    state.db.commit()
    return success(message="Dokumen dihapus")


ROUTE_DEFINITIONS = [
    ("GET", "/api/log-peninjauan", list_log, "view_all"),
    ("POST", "/api/log-peninjauan", create_log, "manage_log"),
    ("GET", "/api/log-peninjauan/<int:record_id>", get_log, "view_all"),
    ("POST", "/api/log-peninjauan/<int:record_id>/upload", upload_bukti, "upload_bukti"),
    ("DELETE", "/api/dokumen-bukti/<int:record_id>", delete_dokumen, "manage_log"),
]
