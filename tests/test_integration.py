"""
Integration test end-to-end (Sprint 2 & 3):
- BUG-3: dashboard tidak membocorkan password_hash.
- MODUL 1: referensi 3 sumber tersimpan & bertahan.
- BUG-4: view turunan default ke periode aktif (berisi data), bukan draft kosong.
- BUG-6: periode terkunci memblokir toggle matriks & penyimpanan penilaian.
- MODUL 9: export Excel peta referensi menghasilkan file .xlsx valid.

Menggunakan SQLite sementara agar tidak menyentuh DB dev/prod.
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _make_client():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["DATABASE_URI"] = "sqlite:///" + path

    # Import setelah env di-set agar config memakai URI sementara.
    import importlib
    import config
    importlib.reload(config)
    import app as app_module
    importlib.reload(app_module)

    application = app_module.create_app()
    app_module.seed_all()
    client = application.test_client()
    client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    return client, app_module, path


def _cleanup(app_module, path):
    try:
        from db.connection import close_db
        close_db()
    except Exception:
        pass
    try:
        os.remove(path)
    except Exception:
        pass


def test_dashboard_no_password_leak():
    client, app_module, path = _make_client()
    try:
        d = client.get("/api/dashboard").get_json()["data"]
        assert "password_hash" not in d["user"], "password_hash bocor di /api/dashboard"
        print("test_dashboard_no_password_leak: OK")
    finally:
        _cleanup(app_module, path)


def test_three_reference_persist():
    client, app_module, path = _make_client()
    try:
        r = client.post("/api/cpl-prodi", json={
            "periode_id": 1, "kode": "CPLREF", "deskripsi": "x",
            "ref_buku": "Tabel 2 hal 17", "ref_spreadsheet": "Sheet CPL", "ref_pikobe": "PK-1",
        })
        assert r.status_code == 201
        d = r.get_json()["data"]
        rid = d["id"]
        found = [x for x in client.get("/api/cpl-prodi?periode_id=1").get_json()["data"]
                 if x["id"] == rid][0]
        assert found["ref_buku"] == "Tabel 2 hal 17"
        assert found["ref_spreadsheet"] == "Sheet CPL"
        assert found["ref_pikobe"] == "PK-1"
        print("test_three_reference_persist: OK")
    finally:
        _cleanup(app_module, path)


def test_derived_view_defaults_to_active_periode():
    client, app_module, path = _make_client()
    try:
        rows = client.get("/api/peta-cpl").get_json()["data"]["rows"]
        assert len(rows) > 0, "peta-cpl default seharusnya berisi data periode aktif"
        empty = client.get("/api/organisasi-mk?periode_id=2").get_json()["data"]
        assert empty == [], "periode draft (2) seharusnya kosong"
        print("test_derived_view_defaults_to_active_periode: OK")
    finally:
        _cleanup(app_module, path)


def test_locked_periode_blocks_writes():
    client, app_module, path = _make_client()
    try:
        import state
        from models.period import PeriodeKurikulum
        from models.cpl import CPLProdi
        cpl = state.db.query(CPLProdi).first()
        pid = cpl.periode_id
        cpl_id = cpl.id

        client.post("/api/periode/%d/lock" % pid)
        r = client.post("/api/matrix/cpl_pl/toggle", json={"row_id": cpl_id, "col_id": 1})
        assert r.status_code == 423, "toggle matriks harus diblokir saat periode terkunci"
        rp = client.post("/api/penilaian/bobot", json={
            "records": [{"cpl_id": 1, "mk_id": 1, "cpmk_id": 1, "total": 100}]
        })
        assert rp.status_code == 423, "penilaian harus diblokir saat periode terkunci"

        client.post("/api/periode/%d/unlock" % pid)
        r2 = client.post("/api/matrix/cpl_pl/toggle", json={"row_id": cpl_id, "col_id": 1})
        assert r2.status_code == 200, "toggle matriks harus jalan setelah unlock"
        print("test_locked_periode_blocks_writes: OK")
    finally:
        _cleanup(app_module, path)


def test_referensi_export_xlsx():
    client, app_module, path = _make_client()
    try:
        r = client.get("/api/referensi/export")
        assert r.status_code == 200
        assert r.data[:2] == b"PK", "output bukan file xlsx (zip) yang valid"
        print("test_referensi_export_xlsx: OK")
    finally:
        _cleanup(app_module, path)


def test_periode_lima_tahun():
    # PERIODE KURIKULUM PER 5 TAHUN (mis. 2024-2028 = 5 tahun inklusif).
    client, app_module, path = _make_client()
    try:
        periodes = client.get("/api/periode").get_json()["data"]
        assert periodes, "daftar periode kosong"
        aktif = [p for p in periodes if p.get("status") == "aktif"] or periodes
        p = aktif[0]
        durasi = int(p["tahun_selesai"]) - int(p["tahun_mulai"]) + 1
        assert durasi == 5, "periode harus 5 tahun, dapat %d (%s-%s)" % (
            durasi, p["tahun_mulai"], p["tahun_selesai"])
        print("test_periode_lima_tahun: OK")
    finally:
        _cleanup(app_module, path)


def test_rps_template_dan_lock():
    # RPS menerima field sesuai template (bukan hanya MK/kode/dosen/deskripsi),
    # bisa diedit lewat endpoint header baru, dan diblokir saat periode terkunci.
    client, app_module, path = _make_client()
    try:
        payload = {
            "mk_id": 1, "periode_id": 1,
            "kode_dokumen": "RPS-T1", "dosen_pengampu": "Dosen A",
            "dosen_koordinator": "Koor B", "tanggal_penyusunan": "01-09-2025",
            "bobot_teori_sks": 2, "bobot_praktikum_sks": 1,
            "mk_prasyarat": "Tidak ada", "deskripsi_singkat": "desk",
            "pustaka_utama": "Buku X", "pustaka_pendukung": "Buku Y",
        }
        r = client.post("/api/rps", json=payload)
        assert r.status_code == 201, "gagal membuat RPS"
        rid = r.get_json()["data"]["id"]

        got = client.get("/api/rps/%d" % rid).get_json()["data"]
        assert got["bobot_teori_sks"] == 2 and got["pustaka_utama"] == "Buku X", \
            "field template RPS tidak tersimpan"

        up = client.put("/api/rps/%d" % rid, json={"kode_dokumen": "RPS-T1-rev", "bobot_praktikum_sks": 2})
        assert up.status_code == 200, "endpoint edit header RPS gagal"
        got2 = client.get("/api/rps/%d" % rid).get_json()["data"]
        assert got2["kode_dokumen"] == "RPS-T1-rev" and got2["bobot_praktikum_sks"] == 2

        client.post("/api/periode/1/lock")
        blocked = client.put("/api/rps/%d" % rid, json={"kode_dokumen": "X"})
        assert blocked.status_code == 423, "edit RPS harus diblokir saat periode terkunci"
        client.post("/api/periode/1/unlock")
        print("test_rps_template_dan_lock: OK")
    finally:
        _cleanup(app_module, path)


if __name__ == "__main__":
    test_dashboard_no_password_leak()
    test_three_reference_persist()
    test_derived_view_defaults_to_active_periode()
    test_locked_periode_blocks_writes()
    test_referensi_export_xlsx()
    test_periode_lima_tahun()
    test_rps_template_dan_lock()
    print("\nSemua test integrasi PASSED.")
