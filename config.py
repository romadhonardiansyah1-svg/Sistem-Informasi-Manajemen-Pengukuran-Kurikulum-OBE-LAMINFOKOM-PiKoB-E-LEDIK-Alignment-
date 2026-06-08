"""
Konfigurasi aplikasi Sistem Informasi Kurikulum OBE.
Seluruh konstanta dan parameter terpusat di file ini.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# -- Database --
# Mode: "sqlite" (default), "mysql" (Laragon), atau "supabase" (PostgreSQL cloud)
# Set environment variable DB_MODE untuk memilih.
# Untuk Supabase, set DATABASE_URL dari dashboard Supabase.

DB_MODE = os.environ.get("DB_MODE", "")

# Jika user salah memasukkan connection string ke dalam DB_MODE
if DB_MODE.startswith("postgresql://") or DB_MODE.startswith("postgres://"):
    os.environ["DATABASE_URL"] = DB_MODE
    DB_MODE = "supabase"
elif not DB_MODE or DB_MODE not in ["sqlite", "mysql", "supabase"]:
    if os.environ.get("DATABASE_URL"):
        DB_MODE = "supabase"
    else:
        DB_MODE = "sqlite"


# Konfigurasi MySQL Laragon
MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_DB = os.environ.get("MYSQL_DB", "sistem_kurikulum_obe")

_MYSQL_URI = (
    "mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"
    .format(
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        db=MYSQL_DB,
    )
)

# SQLite: gunakan /tmp/ di Vercel (filesystem read-only kecuali /tmp/)
_IS_VERCEL = os.environ.get("VERCEL", "") == "1"
_SQLITE_DIR = "/tmp" if _IS_VERCEL else BASE_DIR
_SQLITE_URI = "sqlite:///" + os.path.join(_SQLITE_DIR, "kurikulum_obe.db")

# Supabase: ambil dari DATABASE_URL environment variable
_SUPABASE_URI = os.environ.get("DATABASE_URL", "")

_DB_URI_MAP = {
    "sqlite": _SQLITE_URI,
    "mysql": _MYSQL_URI,
    "supabase": _SUPABASE_URI,
}

DATABASE_URI = os.environ.get(
    "DATABASE_URI",
    _DB_URI_MAP.get(DB_MODE, _SQLITE_URI),
)

# Normalisasi dan validasi URI Database
if DATABASE_URI:
    # 1. Konversi postgres:// menjadi postgresql:// untuk kompatibilitas SQLAlchemy
    if DATABASE_URI.startswith("postgres://"):
        DATABASE_URI = DATABASE_URI.replace("postgres://", "postgresql://", 1)
        
    # 2. Otomatis url-encode password jika mengandung karakter spesial seperti @
    if DATABASE_URI.startswith("postgresql://") or DATABASE_URI.startswith("mysql://"):
        from urllib.parse import quote_plus
        try:
            scheme, rest = DATABASE_URI.split("://", 1)
            if "@" in rest:
                auth, host_db = rest.rsplit("@", 1)
                if ":" in auth:
                    username, password = auth.split(":", 1)
                    if "%" not in password:
                        safe_password = quote_plus(password)
                        DATABASE_URI = f"{scheme}://{username}:{safe_password}@{host_db}"
        except Exception:
            pass

    # 3. Supabase: Jika menggunakan direct host (db.xxxx.supabase.co), otomatis ubah ke IPv4 Pooler host
    # karena Vercel serverless tidak mendukung IPv6 outbound.
    if ".supabase.co" in DATABASE_URI and "db." in DATABASE_URI:
        try:
            scheme, rest = DATABASE_URI.split("://", 1)
            if "@" in rest:
                auth, host_db = rest.rsplit("@", 1)
                # Tambahkan port default jika tidak ada
                if "/" in host_db:
                    host_port, db_name = host_db.split("/", 1)
                else:
                    host_port, db_name = host_db, "postgres"
                
                # Ekstrak project ref
                host_only = host_port.split(":")[0]
                if host_only.startswith("db."):
                    project_ref = host_only.split(".")[1]
                    
                    # Buat username pooler baru (format: postgres.[project-ref])
                    if ":" in auth:
                        username, password = auth.split(":", 1)
                        if not username.endswith(f".{project_ref}"):
                            username = f"{username}.{project_ref}"
                        auth = f"{username}:{password}"
                    
                    # Ganti host ke pooler IPv4
                    new_host = "aws-1-ap-southeast-1.pooler.supabase.com:5432"
                    # Tambahkan SSL param di URL jika belum ada
                    if "?" not in db_name:
                        db_name += "?sslmode=require"
                    DATABASE_URI = f"{scheme}://{auth}@{new_host}/{db_name}"
        except Exception:
            pass

    # 4. Supabase: gunakan Session mode pooler (port 5432) bukan Transaction mode (port 6543)
    if "pooler.supabase.com" in DATABASE_URI:
        DATABASE_URI = DATABASE_URI.replace(":6543/", ":5432/")

    # 5. Otomatis tambahkan sslmode=require untuk koneksi Supabase agar SSL stabil
    if "supabase.co" in DATABASE_URI or "supabase.com" in DATABASE_URI:
        if "?" not in DATABASE_URI:
            DATABASE_URI += "?sslmode=require"
        elif "sslmode=" not in DATABASE_URI:
            DATABASE_URI += "&sslmode=require"



    # 4. Cek jika menggunakan HTTP/HTTPS URL (biasanya Supabase API URL, bukan DB URI)

    if DATABASE_URI.startswith("https://") or DATABASE_URI.startswith("http://"):
        raise ValueError(
            "DATABASE_URI / DATABASE_URL is set to an HTTP/HTTPS URL (starts with https:// or http://). "

            "SQLAlchemy requires a direct database connection URI starting with 'postgresql://' or 'postgres://'. "
            "Please go to your Supabase Dashboard > Project Settings > Database > Connection string > URI, "
            "copy the URI (replace [YOUR-PASSWORD] with your DB password), and update the Vercel environment variable."
        )

DATABASE_ECHO = os.environ.get("DATABASE_ECHO", "false").lower() == "true"



# -- Flask --

SECRET_KEY = os.environ.get("SECRET_KEY", "ganti-dengan-key-yang-aman-di-production")

SESSION_LIFETIME_MINUTES = 120


# -- Pagination --

DEFAULT_PAGE_SIZE = 25

MAX_PAGE_SIZE = 100


# -- Upload --

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

ALLOWED_EXTENSIONS = {"pdf"}

MAX_UPLOAD_SIZE_MB = 10


# -- Supabase Storage (penyimpanan file PDF persisten) --
# Di Vercel, filesystem bersifat read-only/ephemeral, sehingga file PDF
# (notulensi, bukti fisik, dokumen reuni) disimpan ke Supabase Storage.
# Jika SUPABASE_URL & SUPABASE_SERVICE_KEY tidak di-set (mis. dev lokal),
# storage_service otomatis fallback ke disk lokal (UPLOAD_DIR).
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get(
    "SUPABASE_SERVICE_KEY",
    os.environ.get("SUPABASE_KEY", ""),
)
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "obe-dokumen")


# -- Keamanan endpoint diagnostik --
# Token wajib untuk mengakses detail/aksi berbahaya di /api/db-status.
DB_ADMIN_TOKEN = os.environ.get("DB_ADMIN_TOKEN", "")


# -- Jenis Agenda Penjaminan Mutu (modul dokumen/notulensi/reuni) --
JENIS_AGENDA = (
    "peninjauan_kurikulum",
    "reuni_alumni",
    "fgd_lokakarya",
    "rapat_mutu",
)

JENIS_AGENDA_LABELS = {
    "peninjauan_kurikulum": "Peninjauan Kurikulum",
    "reuni_alumni": "Reuni Alumni",
    "fgd_lokakarya": "FGD / Lokakarya",
    "rapat_mutu": "Rapat Mutu",
}


# -- Periode --

PERIODE_DURATION_YEARS = 5


# -- Penilaian --

SKOR_PEMENUHAN_CPL_MINIMAL = 70

BOBOT_TOTAL_PER_MK = 100

RUBRIK_GRADE_RANGES = {
    (81, 100): "Sangat Kompeten",
    (61, 80): "Kompeten",
    (41, 60): "Cukup Kompeten",
    (21, 40): "Kurang Kompeten",
    (0, 20): "Tidak Kompeten",
}


# -- Role --

ROLES = (
    "admin_universitas",
    "dekan",
    "kaprodi",
    "tim_kurikulum",
    "dosen",
    "mahasiswa",
)

# Label role yang ramah untuk ditampilkan di UI.
ROLE_LABELS = {
    "admin_universitas": "Admin Universitas",
    "dekan": "Dekan / Fakultas",
    "kaprodi": "Kaprodi",
    "tim_kurikulum": "Tim Kurikulum",
    "dosen": "Dosen / DPA",
    "mahasiswa": "Mahasiswa",
}


# -- Teknik Penilaian --

TEKNIK_PENILAIAN_COLUMNS = (
    "partisipasi",
    "observasi",
    "unjuk_kerja",
    "tes_tulis_uts",
    "tes_tulis_uas",
    "tes_lisan",
)

TEKNIK_PENILAIAN_LABELS = {
    "partisipasi": "Partisipasi (Quiz)",
    "observasi": "Observasi (Praktek / Tugas)",
    "unjuk_kerja": "Unjuk Kerja (Presentasi)",
    "tes_tulis_uts": "Tes Tulis (UTS)",
    "tes_tulis_uas": "Tes Tulis (UAS)",
    "tes_lisan": "Tes Lisan (Tugas Kelompok)",
}


# -- Instrumen Penilaian --

INSTRUMEN_CHOICES = (
    "rubrik_holistik",
    "rubrik_analitik",
    "rubrik_skala_persepsi",
    "penilaian_portofolio",
)


# -- Tahap Penilaian --

TAHAP_PENILAIAN_CHOICES = (
    "awal_tengah",
    "tengah_akhir",
    "awal_akhir",
)


# -- Jenis Mata Kuliah --

JENIS_MK = (
    "wajib",
    "pilihan",
    "mkwk",
    "mkdu",
)


# -- Kategori Bahan Kajian --

KATEGORI_BK = (
    "utama",
    "pendukung",
)


# -- Kategori CPL SN-Dikti --

KATEGORI_CPL_SNDIKTI = (
    "S",    # Sikap
    "KU",   # Keterampilan Umum
    "KK",   # Keterampilan Khusus
    "P",    # Pengetahuan
)
