"""
Permission resolver menggunakan dispatch table.
Tidak ada if-else bertingkat. Penambahan role cukup menambah entry di dictionary.

Taksonomi action dipisah antara BACA (view_*) dan TULIS (manage_* / input_nilai / lock_*):

  view_kurikulum    : membaca dokumen kurikulum PLAN/DO (identitas, PL, CPL, BK, MK,
                      CPMK, matriks, pemetaan, organisasi, RPS, rumusan, dashboard, periode).
  view_report       : membaca laporan/kalkulasi CPL (staf: kaprodi, dosen, dekan, dll).
  view_report_self  : mahasiswa membaca laporan CPL miliknya sendiri.
  view_dokumen      : membaca Agenda Penjaminan Mutu & dokumen bukti.

  manage_master     : CRUD master data (PL/CPL/BK/MK/CPMK/Sub-CPMK).
  manage_prodi      : ubah identitas/profil program studi.
  manage_matrix     : toggle relasi matriks pemetaan.
  manage_periode    : kelola periode kurikulum (5 tahunan).
  manage_rps        : kelola RPS.
  manage_penilaian  : kelola teknik & tahap penilaian.
  manage_bobot      : kelola bobot penilaian.
  input_nilai       : input nilai aktivitas mahasiswa + kalkulasi.
  lock_periode      : mengunci periode kurikulum.
  manage_users      : kelola akun pengguna (dosen/mahasiswa).
  manage_dokumen    : kelola Agenda Penjaminan Mutu + upload/hapus dokumen (PDF).
"""

ROLE_ACTIONS = {
    "admin_universitas": {
        "scope": "universitas",
        "allowed": {
            "view_kurikulum",
            "view_report",
            "view_dokumen",
            "manage_users",
        },
    },
    "dekan": {
        "scope": "fakultas",
        "allowed": {
            "view_kurikulum",
            "view_report",
            "view_dokumen",
        },
    },
    "kaprodi": {
        "scope": "prodi",
        "allowed": {
            "view_kurikulum",
            "view_report",
            "view_report_self",
            "view_dokumen",
            "manage_master",
            "manage_prodi",
            "manage_matrix",
            "manage_periode",
            "manage_rps",
            "manage_penilaian",
            "manage_bobot",
            "input_nilai",
            "lock_periode",
            "manage_users",
            "manage_dokumen",
        },
    },
    # Tim Kurikulum: hanya kelola master data & matriks (sesuai keputusan klien).
    "tim_kurikulum": {
        "scope": "prodi",
        "allowed": {
            "view_kurikulum",
            "view_report",
            "view_dokumen",
            "manage_master",
            "manage_prodi",
            "manage_matrix",
        },
    },
    "dosen": {
        "scope": "mk_assigned",
        "allowed": {
            "view_kurikulum",
            "view_report",
            "view_dokumen",
            "manage_rps",
            "input_nilai",
        },
    },
    "mahasiswa": {
        "scope": "self",
        "allowed": {
            "view_report_self",
        },
    },
}


def check_permission(role, action):
    """
    Memeriksa apakah role tertentu memiliki akses ke action.
    Return: True/False.
    """
    entry = ROLE_ACTIONS.get(role)
    if entry is None:
        return False
    return action in entry["allowed"]


def get_scope(role):
    """Mengambil scope akses untuk role tertentu."""
    entry = ROLE_ACTIONS.get(role)
    if entry is None:
        return None
    return entry["scope"]


def get_allowed_actions(role):
    """Mengambil seluruh action yang diizinkan untuk role (sebagai list, agar JSON-serializable)."""
    entry = ROLE_ACTIONS.get(role)
    if entry is None:
        return []
    return sorted(entry["allowed"])


def get_all_roles():
    """Mengambil seluruh role yang terdaftar."""
    return list(ROLE_ACTIONS.keys())
