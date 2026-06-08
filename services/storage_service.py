"""
Layanan penyimpanan file PDF.

Strategi:
- Jika SUPABASE_URL + SUPABASE_SERVICE_KEY tersedia -> simpan ke Supabase Storage
  (persisten; cocok untuk Vercel yang filesystem-nya ephemeral).
- Jika tidak (mis. dev lokal) -> simpan ke disk lokal (config.UPLOAD_DIR).

Hanya menggunakan pustaka standar (urllib) agar tidak menambah dependency.
"""

import os
import json
import time
import uuid
import urllib.request
import urllib.error

import config


def is_supabase_enabled():
    return bool(config.SUPABASE_URL and config.SUPABASE_SERVICE_KEY)


def _safe_name(filename):
    """Membuat nama file unik & aman (cegah tabrakan/traversal)."""
    base = os.path.basename(filename or "dokumen.pdf")
    base = base.replace("\\", "_").replace("/", "_").replace(" ", "_")
    stamp = time.strftime("%Y%m%d%H%M%S") + "-" + uuid.uuid4().hex[:8]
    return stamp + "_" + base


def _supabase_headers(extra=None):
    headers = {
        "Authorization": "Bearer " + config.SUPABASE_SERVICE_KEY,
        "apikey": config.SUPABASE_SERVICE_KEY,
    }
    if extra:
        headers.update(extra)
    return headers


def save_pdf(file_storage, folder):
    """
    Menyimpan satu file (werkzeug FileStorage) dan mengembalikan metadata:
        {filename, storage_key, storage_backend, filepath, ukuran}
    Validasi ekstensi PDF & ukuran dilakukan di sini.
    Raise ValueError bila tidak valid.
    """
    filename = file_storage.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in config.ALLOWED_EXTENSIONS:
        raise ValueError("Format file tidak diizinkan. Hanya PDF.")

    data = file_storage.read()
    max_bytes = config.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(data) > max_bytes:
        raise ValueError("Ukuran file melebihi " + str(config.MAX_UPLOAD_SIZE_MB) + " MB.")

    safe = _safe_name(filename)
    key = folder.strip("/") + "/" + safe

    if is_supabase_enabled():
        url = config.SUPABASE_URL.rstrip("/") + "/storage/v1/object/" + config.SUPABASE_BUCKET + "/" + key
        req = urllib.request.Request(
            url,
            data=data,
            method="POST",
            headers=_supabase_headers({
                "Content-Type": "application/pdf",
                "x-upsert": "true",
            }),
        )
        try:
            urllib.request.urlopen(req, timeout=30)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")
            raise ValueError("Gagal mengunggah ke Supabase Storage: " + detail)
        return {
            "filename": filename,
            "storage_key": key,
            "storage_backend": "supabase",
            "filepath": "",
            "ukuran": len(data),
        }

    # Fallback lokal
    target_dir = os.path.join(config.UPLOAD_DIR, *folder.strip("/").split("/"))
    os.makedirs(target_dir, exist_ok=True)
    filepath = os.path.join(target_dir, safe)
    with open(filepath, "wb") as f:
        f.write(data)
    return {
        "filename": filename,
        "storage_key": key,
        "storage_backend": "local",
        "filepath": filepath,
        "ukuran": len(data),
    }


def signed_url(storage_key, expires_in=3600):
    """URL ber-token untuk mengunduh file dari Supabase Storage."""
    url = (
        config.SUPABASE_URL.rstrip("/")
        + "/storage/v1/object/sign/"
        + config.SUPABASE_BUCKET
        + "/"
        + storage_key
    )
    body = json.dumps({"expiresIn": expires_in}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers=_supabase_headers({"Content-Type": "application/json"}),
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    signed = payload.get("signedURL") or payload.get("signedUrl") or ""
    return config.SUPABASE_URL.rstrip("/") + "/storage/v1" + signed


def delete_file(doc):
    """Menghapus file fisik sesuai backend penyimpanannya."""
    backend = getattr(doc, "storage_backend", "local")
    if backend == "supabase":
        url = (
            config.SUPABASE_URL.rstrip("/")
            + "/storage/v1/object/"
            + config.SUPABASE_BUCKET
            + "/"
            + (doc.storage_key or "")
        )
        req = urllib.request.Request(url, method="DELETE", headers=_supabase_headers())
        try:
            urllib.request.urlopen(req, timeout=30)
        except urllib.error.HTTPError:
            pass
        return

    path = getattr(doc, "filepath", "") or ""
    if path and os.path.exists(path):
        os.remove(path)
