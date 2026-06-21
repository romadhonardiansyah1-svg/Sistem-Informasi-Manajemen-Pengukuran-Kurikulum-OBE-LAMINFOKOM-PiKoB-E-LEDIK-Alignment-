-- =====================================================================
-- MIGRASI SUPABASE — Tambah kolom baru tanpa menghapus data
-- =====================================================================
-- Jalankan SATU KALI di Supabase SQL Editor.
-- Aman & idempotent: memakai "ADD COLUMN IF NOT EXISTS", boleh diulang.
-- TIDAK menghapus tabel / data yang sudah ada (66 MK, CPL, BK, dst tetap aman).
--
-- Konteks: model aplikasi menambah kolom referensi 3 sumber (ref_buku,
-- ref_spreadsheet, ref_pikobe) + beberapa kolom lain. Di Vercel,
-- create_all()/ensure_columns() dilewati, sehingga kolom ini belum ada di
-- Supabase. Akibatnya SELECT (mis. /api/mk) gagal "column does not exist"
-- dan halaman tampak kosong. Skrip ini menambal kolom tersebut.
-- =====================================================================

-- ---- Profil Lulusan ----
ALTER TABLE profil_lulusan ADD COLUMN IF NOT EXISTS referensi TEXT;
ALTER TABLE profil_lulusan ADD COLUMN IF NOT EXISTS kategori VARCHAR(50);
ALTER TABLE profil_lulusan ADD COLUMN IF NOT EXISTS ref_buku TEXT;
ALTER TABLE profil_lulusan ADD COLUMN IF NOT EXISTS ref_spreadsheet TEXT;
ALTER TABLE profil_lulusan ADD COLUMN IF NOT EXISTS ref_pikobe TEXT;

-- ---- CPL Prodi ----
ALTER TABLE cpl_prodi ADD COLUMN IF NOT EXISTS referensi TEXT;
ALTER TABLE cpl_prodi ADD COLUMN IF NOT EXISTS ref_buku TEXT;
ALTER TABLE cpl_prodi ADD COLUMN IF NOT EXISTS ref_spreadsheet TEXT;
ALTER TABLE cpl_prodi ADD COLUMN IF NOT EXISTS ref_pikobe TEXT;

-- ---- CPL SN-Dikti ----
ALTER TABLE cpl_sn_dikti ADD COLUMN IF NOT EXISTS referensi TEXT;

-- ---- Bahan Kajian ----
ALTER TABLE bahan_kajian ADD COLUMN IF NOT EXISTS referensi TEXT;
ALTER TABLE bahan_kajian ADD COLUMN IF NOT EXISTS ref_buku TEXT;
ALTER TABLE bahan_kajian ADD COLUMN IF NOT EXISTS ref_spreadsheet TEXT;
ALTER TABLE bahan_kajian ADD COLUMN IF NOT EXISTS ref_pikobe TEXT;

-- ---- Mata Kuliah ----
ALTER TABLE mata_kuliah ADD COLUMN IF NOT EXISTS jenis VARCHAR(20) DEFAULT 'wajib';
ALTER TABLE mata_kuliah ADD COLUMN IF NOT EXISTS is_capstone BOOLEAN DEFAULT FALSE;
ALTER TABLE mata_kuliah ADD COLUMN IF NOT EXISTS prasyarat TEXT;
ALTER TABLE mata_kuliah ADD COLUMN IF NOT EXISTS deskripsi_singkat TEXT;
ALTER TABLE mata_kuliah ADD COLUMN IF NOT EXISTS referensi TEXT;
ALTER TABLE mata_kuliah ADD COLUMN IF NOT EXISTS ref_buku TEXT;
ALTER TABLE mata_kuliah ADD COLUMN IF NOT EXISTS ref_spreadsheet TEXT;
ALTER TABLE mata_kuliah ADD COLUMN IF NOT EXISTS ref_pikobe TEXT;

-- ---- CPMK ----
ALTER TABLE cpmk ADD COLUMN IF NOT EXISTS referensi TEXT;
ALTER TABLE cpmk ADD COLUMN IF NOT EXISTS ref_buku TEXT;
ALTER TABLE cpmk ADD COLUMN IF NOT EXISTS ref_spreadsheet TEXT;
ALTER TABLE cpmk ADD COLUMN IF NOT EXISTS ref_pikobe TEXT;

-- ---- Log Peninjauan ----
ALTER TABLE log_peninjauan ADD COLUMN IF NOT EXISTS jenis VARCHAR(40) DEFAULT 'peninjauan_kurikulum';
ALTER TABLE log_peninjauan ADD COLUMN IF NOT EXISTS periode_id INTEGER;
ALTER TABLE log_peninjauan ADD COLUMN IF NOT EXISTS lokasi VARCHAR(200);

-- ---- Dokumen Bukti ----
ALTER TABLE dokumen_bukti ADD COLUMN IF NOT EXISTS storage_key VARCHAR(500) DEFAULT '';
ALTER TABLE dokumen_bukti ADD COLUMN IF NOT EXISTS storage_backend VARCHAR(20) DEFAULT 'local';

-- ---- Mahasiswa ----
ALTER TABLE mahasiswa ADD COLUMN IF NOT EXISTS user_id INTEGER;

-- ---- RPS ----
ALTER TABLE rps ADD COLUMN IF NOT EXISTS bobot_teori_sks INTEGER DEFAULT 0;
ALTER TABLE rps ADD COLUMN IF NOT EXISTS bobot_praktikum_sks INTEGER DEFAULT 0;
ALTER TABLE rps ADD COLUMN IF NOT EXISTS media_software TEXT;
ALTER TABLE rps ADD COLUMN IF NOT EXISTS media_hardware TEXT;
ALTER TABLE rps ADD COLUMN IF NOT EXISTS mk_prasyarat TEXT;

-- =====================================================================
-- Backfill: salin nilai 'referensi' lama -> 'ref_buku' bila ref_buku kosong.
-- =====================================================================
UPDATE profil_lulusan SET ref_buku = referensi WHERE ref_buku IS NULL AND referensi IS NOT NULL;
UPDATE cpl_prodi      SET ref_buku = referensi WHERE ref_buku IS NULL AND referensi IS NOT NULL;
UPDATE bahan_kajian   SET ref_buku = referensi WHERE ref_buku IS NULL AND referensi IS NOT NULL;

-- =====================================================================
-- Verifikasi cepat (opsional): pastikan data MK ada & kolom baru terbaca.
-- SELECT id, kode, nama, ref_buku, ref_spreadsheet, ref_pikobe
-- FROM mata_kuliah ORDER BY semester, kode LIMIT 5;
-- =====================================================================
