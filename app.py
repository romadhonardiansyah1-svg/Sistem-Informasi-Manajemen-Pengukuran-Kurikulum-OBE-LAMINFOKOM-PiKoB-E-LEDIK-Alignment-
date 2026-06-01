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
        import config
        import state
        from sqlalchemy import inspect
        
        status = {
            "db_mode": config.DB_MODE,
            "database_uri_masked": "",
            "connection_ok": False,
            "error": None,
            "tables": []
        }
        
        uri = config.DATABASE_URI or ""
        if "@" in uri:
            try:
                parts = uri.split("@")
                prefix = parts[0]
                scheme = "postgresql" if "postgresql" in prefix else "mysql" if "mysql" in prefix else "db"
                status["database_uri_masked"] = f"{scheme}://***:***@{parts[1]}"
            except Exception:
                status["database_uri_masked"] = "invalid_uri_format"
        else:
            status["database_uri_masked"] = uri
            
        try:
            conn = state.engine.connect()
            inspector = inspect(state.engine)
            status["tables"] = inspector.get_table_names()
            status["connection_ok"] = True
            
            if "users" in status["tables"]:
                from models.user import User
                admin = state.db.query(User).filter_by(username="admin").first()
                status["admin_user_exists"] = admin is not None
                status["users_count"] = state.db.query(User).count()
                if admin:
                    status["admin_password_hash_empty"] = not bool(admin.password_hash)
            
            conn.close()
        except Exception as e:
            status["error"] = str(e)
            
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

    # Data kurikulum
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

        # RPS dan Mahasiswa
        seed_rps(periode_id)
        seed_mahasiswa(prodi_id)

        session.commit()
        print("Seed data selesai: 5 PL, 14 CPL, 21 BK, 66 MK, 33 CPMK, 5 matriks, 3 RPS, 5 mahasiswa.")
    except Exception as e:
        session.rollback()
        print(f"Seeding kurikulum dilewati atau gagal (kemungkinan data sudah ada): {e}")



if __name__ == "__main__":
    app = create_app()
    seed_all()
    app.run(debug=True, port=5000)
