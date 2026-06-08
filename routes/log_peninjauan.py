"""
Route Agenda Penjaminan Mutu (peninjauan kurikulum, reuni alumni, FGD, rapat mutu).
CRUD agenda + notulensi + upload banyak dokumen bukti fisik (PDF) ke Supabase Storage.
T-13.1 / T-13.2 Backlog.
"""

import os
from datetime import date
from flask import request, send_from_directory, redirect

import config
import state
from models.log_peninjauan import LogPeninjauan, DokumenBukti
from services import storage_service
from utils.response import success, created, not_found, error


def list_log():
    """GET /api/log-peninjauan?jenis=...&periode_id=..."""
    query = state.db.query(LogPeninjauan)

    jenis = request.args.get("jenis")
    if jenis:
        query = query.filter_by(jenis=jenis)

    periode_id = request.args.get("periode_id", type=int)
    if periode_id:
        query = query.filter_by(periode_id=periode_id)

    items = query.order_by(LogPeninjauan.tanggal.desc()).all()
    data = []
    for item in items:
        d = item.to_dict()
        d["dokumen_count"] = item.dokumen_list.count()
        data.append(d)
    return success(data=data)


def create_log():
    """POST /api/log-peninjauan"""
    body = request.get_json(silent=True) or {}
    if not body.get("judul") or not body.get("tanggal"):
        return error("Judul dan tanggal wajib diisi.")

    jenis = body.get("jenis", "peninjauan_kurikulum")
    if jenis not in config.JENIS_AGENDA:
        jenis = "peninjauan_kurikulum"

    log = LogPeninjauan(
        jenis=jenis,
        periode_id=body.get("periode_id"),
        judul=body["judul"],
        tanggal=date.fromisoformat(body["tanggal"]),
        lokasi=body.get("lokasi", ""),
        peserta=body.get("peserta", ""),
        catatan=body.get("catatan", ""),
        status=body.get("status", "draft"),
    )
    state.db.add(log)
    state.db.commit()
    return created(data=log.to_dict())


def update_log(record_id):
    """PUT /api/log-peninjauan/<id>"""
    log = state.db.query(LogPeninjauan).get(record_id)
    if log is None:
        return not_found()

    body = request.get_json(silent=True) or {}
    for field in ("judul", "lokasi", "peserta", "catatan", "status"):
        if body.get(field) is not None:
            setattr(log, field, body[field])
    if body.get("jenis") in config.JENIS_AGENDA:
        log.jenis = body["jenis"]
    if body.get("periode_id") is not None:
        log.periode_id = body["periode_id"]
    if body.get("tanggal"):
        log.tanggal = date.fromisoformat(body["tanggal"])

    state.db.commit()
    return success(data=log.to_dict(), message="Agenda diperbarui")


def get_log(record_id):
    """GET /api/log-peninjauan/<id>"""
    log = state.db.query(LogPeninjauan).get(record_id)
    if log is None:
        return not_found()

    d = log.to_dict()
    d["dokumen"] = [doc.to_dict() for doc in log.dokumen_list.all()]
    return success(data=d)


def delete_log(record_id):
    """DELETE /api/log-peninjauan/<id> (beserta dokumennya)"""
    log = state.db.query(LogPeninjauan).get(record_id)
    if log is None:
        return not_found()

    for doc in log.dokumen_list.all():
        storage_service.delete_file(doc)

    state.db.delete(log)
    state.db.commit()
    return success(message="Agenda dihapus")


def upload_bukti(record_id):
    """POST /api/log-peninjauan/<id>/upload (multiple PDF)"""
    log = state.db.query(LogPeninjauan).get(record_id)
    if log is None:
        return not_found()

    files = request.files.getlist("files")
    if not files:
        return error("Tidak ada file yang dikirim")

    uploaded = []
    skipped = []
    folder = "agenda/" + str(record_id)

    for f in files:
        if not f or not f.filename:
            continue
        try:
            meta = storage_service.save_pdf(f, folder)
        except ValueError as e:
            skipped.append(f.filename + " (" + str(e) + ")")
            continue

        doc = DokumenBukti(
            log_id=record_id,
            filename=meta["filename"],
            filepath=meta["filepath"],
            storage_key=meta["storage_key"],
            storage_backend=meta["storage_backend"],
            ukuran=meta["ukuran"],
        )
        state.db.add(doc)
        uploaded.append(meta["filename"])

    state.db.commit()
    return created(
        data={"uploaded": uploaded, "skipped": skipped, "count": len(uploaded)},
        message=str(len(uploaded)) + " file berhasil diunggah",
    )


def download_dokumen(record_id):
    """GET /api/dokumen-bukti/<id>/download -> redirect signed URL (supabase) / kirim file (local)"""
    doc = state.db.query(DokumenBukti).get(record_id)
    if doc is None:
        return not_found()

    if doc.storage_backend == "supabase":
        return redirect(storage_service.signed_url(doc.storage_key))

    if doc.filepath and os.path.exists(doc.filepath):
        directory = os.path.dirname(doc.filepath)
        fname = os.path.basename(doc.filepath)
        return send_from_directory(directory, fname, as_attachment=True, download_name=doc.filename)

    return not_found("File tidak ditemukan di server.")


def delete_dokumen(record_id):
    """DELETE /api/dokumen-bukti/<id>"""
    doc = state.db.query(DokumenBukti).get(record_id)
    if doc is None:
        return not_found()

    storage_service.delete_file(doc)
    state.db.delete(doc)
    state.db.commit()
    return success(message="Dokumen dihapus")


ROUTE_DEFINITIONS = [
    ("GET", "/api/log-peninjauan", list_log, "view_dokumen"),
    ("POST", "/api/log-peninjauan", create_log, "manage_dokumen"),
    ("GET", "/api/log-peninjauan/<int:record_id>", get_log, "view_dokumen"),
    ("PUT", "/api/log-peninjauan/<int:record_id>", update_log, "manage_dokumen"),
    ("DELETE", "/api/log-peninjauan/<int:record_id>", delete_log, "manage_dokumen"),
    ("POST", "/api/log-peninjauan/<int:record_id>/upload", upload_bukti, "manage_dokumen"),
    ("GET", "/api/dokumen-bukti/<int:record_id>/download", download_dokumen, "view_dokumen"),
    ("DELETE", "/api/dokumen-bukti/<int:record_id>", delete_dokumen, "manage_dokumen"),
]
