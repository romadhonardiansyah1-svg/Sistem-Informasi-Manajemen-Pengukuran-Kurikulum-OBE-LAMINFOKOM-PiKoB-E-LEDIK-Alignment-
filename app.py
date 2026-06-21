"""
Entry point aplikasi Sistem Informasi Kurikulum OBE.
Flask app factory.
"""

import os
from flask import Flask, render_template, redirect, session

import config
import state
from db.connection import init_db, close_db
from db.migrate import create_all
from routes.registry import register_routes


def create_app():
    """Membuat dan mengkonfigurasi Flask app."""
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )

    app.secret_key = config.SECRET_KEY
    state.app = app

    init_db()

    # Di Vercel, skip create_all() karena tabel sudah dibuat di Supabase.
    # create_all() menjalankan DDL yang menyebabkan SSL drop pada pooler.
    _is_vercel = os.environ.get("VERCEL", "") == "1"
    if not _is_vercel:
        try:
            create_all()
        except Exception as e:
            print(f"create_all warning (ignored): {e}")



    register_routes(app)
    _register_page_routes(app)

    app.teardown_appcontext(_teardown)

    # Global error handler: tangkap SEMUA exception dan kembalikan JSON
    # agar frontend tidak pernah menerima HTML 500 dari Flask.
    @app.errorhandler(Exception)
    def handle_exception(e):
        import traceback
        tb = traceback.format_exc()
        print(f"Unhandled exception:\n{tb}")
        return {
            "status": "error",
            "message": f"Server error: {str(e)}",
            "traceback": tb,
        }, 500

    return app




def _register_page_routes(app):
    """Route untuk halaman HTML."""

    @app.route("/")
    def index():
        if "user_id" not in session:
            return redirect("/login")
        return render_template("app.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/api/db-status")
    def db_status():
        """
        Endpoint diagnostik. Status koneksi dasar bersifat publik, namun
        DETAIL SENSITIF (daftar user) dan AKSI BERBAHAYA (reset password / init DB)
        hanya tersedia bila ?token= cocok dengan env DB_ADMIN_TOKEN.
        password_hash tidak pernah dikembalikan.
        """
        import config
        import state
        from flask import request
        from sqlalchemy import inspect

        token = request.args.get("token", "")
        authorized = bool(config.DB_ADMIN_TOKEN) and token == config.DB_ADMIN_TOKEN

        status = {
            "db_mode": config.DB_MODE,
            "connection_ok": False,
            "error": None,
        }

        try:
            conn = state.engine.connect()
            tables = inspect(state.engine).get_table_names()
            status["connection_ok"] = True
            status["tables_count"] = len(tables)
            conn.close()

            if token and not authorized:
                if not config.DB_ADMIN_TOKEN:
                    status["error"] = ("DB_ADMIN_TOKEN belum di-set di environment server (Vercel). "
                                       "Set env var DB_ADMIN_TOKEN lalu Redeploy, baru pakai token itu.")
                    status["token_configured"] = False
                else:
                    status["error"] = "Token tidak valid (tidak cocok dengan DB_ADMIN_TOKEN di server)."
                    status["token_configured"] = True
                return status

            if not authorized:
                # Mode publik: jangan bocorkan struktur/data.
                return status

            # --- Mulai area khusus admin ber-token ---
            from models.user import User
            status["tables"] = tables
            if "users" in tables:
                status["users_count"] = state.db.query(User).count()
                status["users_list"] = [
                    {"username": u.username, "role": u.role, "nama": u.nama}
                    for u in state.db.query(User).all()
                ]

            if request.args.get("reset") == "1":
                from services.auth_service import hash_password
                admin = state.db.query(User).filter_by(username="admin").first()
                if admin:
                    admin.password_hash = hash_password("admin123")
                    state.db.add(admin)
                    state.db.commit()
                    status["reset_status"] = "Password admin direset ke admin123"
                else:
                    status["reset_status"] = "User admin tidak ditemukan"

            if request.args.get("init") == "1":
                create_all()
                force = request.args.get("force") == "1"
                if force:
                    # Re-seed PAKSA: hapus baris lama agar skip-guard seed_all
                    # (yang melewati seeding bila ProgramStudi sudah ada) tidak
                    # menahan pengisian ulang. Berguna saat seed sebelumnya gagal
                    # sebagian (mis. MK kosong) sehingga ?init=1 biasa tidak menambal.
                    from db.migrate import clear_all_data
                    clear_all_data()
                seed_all()
                from models.mata_kuliah import MataKuliah
                from models.cpl import CPLProdi
                status["init_status"] = (
                    ("FORCE: data lama dihapus lalu " if force else "")
                    + "seeding dijalankan"
                )
                status["mk_count"] = state.db.query(MataKuliah).count()
                status["cpl_count"] = state.db.query(CPLProdi).count()
                status["tables"] = inspect(state.engine).get_table_names()

        except Exception as e:
            status["error"] = str(e)
            try:
                state.db.rollback()
            except Exception:
                pass

        return status




def _teardown(exception=None):
    """Cleanup saat request selesai."""
    state.current_user = None
    if state.db:
        state.db.remove()


def seed_all():
    """Seed seluruh data awal jika database masih kosong."""
    from models.user import User
    from services.auth_service import hash_password
    from db.seed import seed_institution, seed_periode, seed_profil_lulusan
    from db.seed_cpl_bk import seed_cpl_prodi, seed_bahan_kajian
    from db.seed_mk import seed_mata_kuliah
    from db.seed_matrix import seed_cpl_pl_matrix, seed_cpl_bk_matrix, seed_bk_mk_matrix
    from db.seed_cpmk import seed_cpmk
    from db.seed_cpmk_mk import seed_cpmk_mk_matrix, seed_cpl_mk_matrix
    from db.seed_rps import seed_rps, seed_mahasiswa
    from db.seed_penilaian import seed_tahap_penilaian, seed_nilai_demo

    session = state.db

    existing = session.query(User).filter_by(username="admin").first()
    if existing is None:
        # User admin
        admin = User(
            username="admin",
            password_hash=hash_password("admin123"),
            nama="Administrator",
            email="admin@prodi.ac.id",
            role="kaprodi",
        )
        session.add(admin)
        try:
            session.commit()
            print("User admin berhasil dibuat secara mandiri.")
        except Exception as e:
            session.rollback()
            print(f"Gagal membuat user admin: {e}")

    # Akun demo per role (idempotent: lewati jika sudah ada)
    demo = [
        ("kaprodi", "kaprodi", "Kaprodi Demo", "kaprodi"),
        ("timkurikulum", "timkurikulum", "Tim Kurikulum Demo", "tim_kurikulum"),
        ("dosen", "dosen", "Dosen Demo", "dosen"),
    ]
    for uname, pw, nama, role in demo:
        if session.query(User).filter_by(username=uname).first() is None:
            session.add(User(
                username=uname,
                password_hash=hash_password(pw),
                nama=nama,
                email=uname + "@prodi.ac.id",
                role=role,
            ))
    try:
        session.commit()
    except Exception:
        session.rollback()

    # Seed data master dropdown (Kategori PL & Jenis MK) — idempotent
    from models.master_dropdown import KategoriPL, JenisMK
    if session.query(KategoriPL).first() is None:
        for nama in ["PL Penciri Utama", "PL Sikap", "PL Keterampilan Umum dan Sikap", "PL Tambahan KK dan P"]:
            session.add(KategoriPL(nama=nama))
    if session.query(JenisMK).first() is None:
        for nama in ["MK Wajib", "MK Pilihan", "MKWK", "MKDU"]:
            session.add(JenisMK(nama=nama))
    try:
        session.commit()
    except Exception:
        session.rollback()

    # Data kurikulum (idempotent: lewati bila kurikulum sudah ada agar
    # ?init=1 yang diulang tidak menduplikasi data).
    from models.institution import ProgramStudi
    if session.query(ProgramStudi).first() is not None:
        print("Data kurikulum sudah ada -> seeding kurikulum dilewati.")
        return

    try:
        prodi_id = seed_institution()
        periode_id = seed_periode(prodi_id)
        seed_profil_lulusan(periode_id)
        seed_cpl_prodi(periode_id)
        seed_bahan_kajian(periode_id)
        seed_mata_kuliah(periode_id)
        seed_cpmk()

        # Matriks pemetaan
        seed_cpl_pl_matrix()
        seed_cpl_bk_matrix()
        seed_bk_mk_matrix()
        seed_cpl_mk_matrix()
        seed_cpmk_mk_matrix()

        # RPS dan Mahasiswa (+ akun login mahasiswa)
        seed_rps(periode_id)
        seed_mahasiswa(prodi_id)

        # Data demo penilaian + nilai agar laporan CPL bernilai nyata (bukan 0)
        seed_tahap_penilaian()
        seed_nilai_demo()

        session.commit()
        print("Seed data selesai: 5 PL, 14 CPL, 21 BK, 66 MK, 33 CPMK, matriks, RPS, 5 mahasiswa + akun, tahap penilaian & nilai demo.")
    except Exception as e:
        session.rollback()
        print(f"Seeding kurikulum dilewati atau gagal (kemungkinan data sudah ada): {e}")



if __name__ == "__main__":
    app = create_app()
    seed_all()
    app.run(debug=True, port=5000)
