# Catatan Deploy — Sistem Kurikulum OBE

Stack: Flask + SQLAlchemy di Vercel (serverless) + Supabase (PostgreSQL) + Supabase Storage (file PDF).

## 1. Environment Variables (Vercel → Project Settings → Environment Variables)

| Variable | Wajib | Keterangan |
|---|---|---|
| `DATABASE_URL` | ✅ | Connection string Postgres dari Supabase (URI). |
| `SECRET_KEY` | ✅ | Kunci sesi Flask (string acak panjang). |
| `DB_ADMIN_TOKEN` | ✅ | Token rahasia untuk endpoint diagnostik `/api/db-status` (reset/init). |
| `SUPABASE_URL` | ✅ | URL project Supabase, mis. `https://xxxx.supabase.co`. |
| `SUPABASE_SERVICE_KEY` | ✅ | **Service role key** Supabase (untuk upload/sign/delete Storage). Simpan rahasia. |
| `SUPABASE_BUCKET` | ➖ | Nama bucket Storage. Default `obe-dokumen`. |
| `VERCEL` | (otomatis) | Di-set Vercel = `1`. |

## 2. Supabase Storage
Buat bucket bernama **`obe-dokumen`** (disarankan **Private**). Aplikasi mengunggah via
service key dan menyajikan unduhan lewat **signed URL** berjangka (endpoint
`GET /api/dokumen-bukti/<id>/download` akan redirect ke signed URL).

## 3. Inisialisasi / Migrasi Database
Setelah set env & deploy, jalankan **sekali**:

```
GET https://<domain>/api/db-status?token=<DB_ADMIN_TOKEN>&init=1
```

Ini akan:
- `create_all()` — membuat tabel yang belum ada (mis. `nilai_mahasiswa`, `tahap_penilaian`).
- `ensure_columns()` — menambah kolom baru pada tabel lama secara idempotent
  (`log_peninjauan.jenis/periode_id/lokasi`, `dokumen_bukti.storage_key/storage_backend`,
  `mahasiswa.user_id`). Aman dijalankan berulang.
- `seed_all()` — mengisi data awal **hanya jika belum ada** (admin & kurikulum di-skip bila sudah ada).

Cek status tanpa aksi (aman, tidak membocorkan data):
```
GET https://<domain>/api/db-status
```

## 4. Akun Demo (hasil seeding)
| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | kaprodi (kontrol penuh) |
| `2024001` … `2024005` | sama dengan NIM | mahasiswa |

Kaprodi dapat membuat akun **dosen / tim kurikulum / mahasiswa** lewat menu
**Administrasi → Manajemen Pengguna** (atau reset password akun yang ada).

## 5. Role & Hak Akses (ringkas)
- **admin_universitas / dekan** — lihat kurikulum, laporan, dokumen (read-only).
- **kaprodi** — kontrol penuh (master, matriks, periode, RPS, penilaian, nilai, dokumen, user, kunci periode).
- **tim_kurikulum** — kelola master data & matriks saja.
- **dosen / DPA** — RPS, input nilai, lihat laporan & dokumen.
- **mahasiswa** — hanya "Laporan Capaian Saya" (radar + tabel CPL + unduh PDF).

## 6. Catatan
- Periode kurikulum dipaksa **5 tahun** (`tahun_selesai = tahun_mulai + 4`).
- Upload **hanya PDF**, maks `MAX_UPLOAD_SIZE_MB` (default 10 MB).
- Lokal (tanpa env Supabase): file otomatis tersimpan ke disk `uploads/` (fallback dev).
