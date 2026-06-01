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

DB_MODE = os.environ.get("DB_MODE", "sqlite")

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
    "dosen",
    "mahasiswa",
)


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
