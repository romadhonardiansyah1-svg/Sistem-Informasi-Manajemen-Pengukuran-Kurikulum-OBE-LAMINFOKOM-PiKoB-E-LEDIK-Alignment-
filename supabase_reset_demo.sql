-- =====================================================================
-- RESET DATA DEMO (penilaian, nilai, RPS) — AMAN
-- =====================================================================
-- CARA TERMUDAH (DISARANKAN) — TANPA SQL Editor:
--   Cukup buka URL ini di browser (sekali):
--       https://<domain-anda>/api/db-status?token=<DB_ADMIN_TOKEN>&reseed_demo=1
--   Endpoint itu otomatis mengosongkan 6 tabel demo lalu mengisinya ulang
--   dengan data lengkap (RPS 16 minggu, penilaian, ratusan nilai bervariasi).
--   Lalu refresh aplikasi (Ctrl+F5).
--
--   Catatan: error "Gagal menjalankan 'removeChild' pada 'Node'" yang muncul
--   saat memakai SQL Editor Supabase adalah GANGGUAN UI dashboard Supabase
--   (akibat fitur terjemahan otomatis browser), BUKAN error SQL. Memakai
--   endpoint di atas menghindari masalah itu sepenuhnya.
--
-- ---------------------------------------------------------------------
-- ALTERNATIF (via Supabase SQL Editor):
--   Jika tetap ingin lewat SQL Editor, MATIKAN dulu terjemahan halaman
--   (klik kanan -> "Jangan terjemahkan halaman ini"), lalu jalankan skrip
--   di bawah. Setelah sukses, panggil ?reseed_demo=1 / ?init=1 untuk mengisi
--   ulang, ATAU biarkan aplikasi mengisi otomatis saat dibuka.
--
-- Tabel yang dikosongkan (data kurikulum inti TIDAK disentuh):
--   rps_minggu, rps, sub_cpmk, nilai_mahasiswa, tahap_penilaian, bobot_penilaian
-- =====================================================================

BEGIN;

-- Urutan aman terhadap foreign key (anak dulu). DELETE dipakai (bukan TRUNCATE)
-- agar lebih kompatibel dan tidak butuh CASCADE.
DELETE FROM rps_minggu;
DELETE FROM rps;
DELETE FROM sub_cpmk;
DELETE FROM nilai_mahasiswa;
DELETE FROM tahap_penilaian;
DELETE FROM bobot_penilaian;

COMMIT;

-- Verifikasi (opsional) — semua harus 0 setelah reset:
-- SELECT
--   (SELECT COUNT(*) FROM rps)               AS rps,
--   (SELECT COUNT(*) FROM rps_minggu)        AS rps_minggu,
--   (SELECT COUNT(*) FROM sub_cpmk)          AS sub_cpmk,
--   (SELECT COUNT(*) FROM nilai_mahasiswa)   AS nilai,
--   (SELECT COUNT(*) FROM tahap_penilaian)   AS tahap,
--   (SELECT COUNT(*) FROM bobot_penilaian)   AS bobot;
