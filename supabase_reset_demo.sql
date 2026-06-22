-- =====================================================================
-- RESET DATA DEMO (penilaian, nilai, RPS) — AMAN
-- =====================================================================
-- Tujuan: mengosongkan HANYA tabel data demo agar bisa diisi ulang dengan
-- data dummy terbaru yang lengkap & profesional. Data kurikulum inti
-- (Profil Lulusan, CPL, Bahan Kajian, Mata Kuliah, CPMK, matriks/pemetaan,
-- periode, user, mahasiswa) TIDAK disentuh.
--
-- Tabel yang dikosongkan:
--   rps_minggu, rps, sub_cpmk, nilai_mahasiswa, tahap_penilaian, bobot_penilaian
--
-- CARA PAKAI (Supabase):
--   1. Buka Supabase -> SQL Editor.
--   2. Jalankan seluruh skrip ini (klik Run). Aman & dalam satu transaksi.
--   3. Setelah sukses, buka URL aplikasi di Vercel:
--          https://<domain-anda>/api/db-status?token=<DB_ADMIN_TOKEN>&init=1
--      (DB_ADMIN_TOKEN = nilai environment variable di Vercel).
--      Endpoint itu akan MENGISI ULANG tabel demo dengan data lengkap:
--      ~147 baris Tahap+Bobot penilaian, ratusan nilai bervariasi,
--      10 RPS x 16 minggu.
--   4. Refresh aplikasi (Ctrl+F5). Laporan & cetak penilaian kini berisi data.
--
-- Catatan: skrip ini idempotent secara praktis — boleh dijalankan berkali-kali.
-- Urutan TRUNCATE sudah memperhatikan foreign key (rps_minggu menunjuk ke rps
-- dan sub_cpmk; semuanya ada dalam satu perintah, jadi tidak perlu CASCADE).
-- =====================================================================

BEGIN;

TRUNCATE TABLE
    rps_minggu,
    rps,
    sub_cpmk,
    nilai_mahasiswa,
    tahap_penilaian,
    bobot_penilaian
RESTART IDENTITY;

COMMIT;

-- Jika muncul error dependency foreign key (mis. ada tabel lain yang menunjuk
-- ke salah satu tabel di atas), ganti perintah TRUNCATE di atas dengan versi
-- CASCADE berikut (hapus tanda komentar):
--
-- BEGIN;
-- TRUNCATE TABLE rps_minggu, rps, sub_cpmk, nilai_mahasiswa,
--                tahap_penilaian, bobot_penilaian
-- RESTART IDENTITY CASCADE;
-- COMMIT;

-- Verifikasi (opsional) — semua harus 0 setelah reset:
-- SELECT
--   (SELECT COUNT(*) FROM rps)               AS rps,
--   (SELECT COUNT(*) FROM rps_minggu)        AS rps_minggu,
--   (SELECT COUNT(*) FROM sub_cpmk)          AS sub_cpmk,
--   (SELECT COUNT(*) FROM nilai_mahasiswa)   AS nilai,
--   (SELECT COUNT(*) FROM tahap_penilaian)   AS tahap,
--   (SELECT COUNT(*) FROM bobot_penilaian)   AS bobot;
