# RENCANA EKSEKUSI REVISI — Sistem Kurikulum OBE

> Versi: Juni 2026 · Basis: review klien (Bu Endang) + Buku Kurikulum SI v2.0 + Rancangan Kurikulum (xlsx) + catatan teman.
> Dokumen ini **berbasis kondisi nyata kode yang sudah diverifikasi**, bukan asumsi greenfield. Banyak fitur ternyata SUDAH jalan; sisa kerja difokuskan ke gap yang benar-benar ada.
> Aturan main: kerjakan **berurutan per sprint**, satu tugas selesai + **diverifikasi end-to-end** baru lanjut. Jangan tinggalkan stub/permission tak terdaftar.

---

## 0. KOREKSI STATUS — sistem TIDAK lagi sekadar "fondasi/epik 3"

Review menyebut sistem "masih fondasi". Hasil audit kode menunjukkan **mayoritas epik sudah terbangun & lulus 14 unit test**. Yang tersisa adalah penyempurnaan terfokus. Tabel di bawah = sumber kebenaran prioritas.

| # | Permintaan review | Status nyata | Bukti / Catatan |
|---|---|---|---|
| 1 | Sidebar collapsible | ✅ DONE | `sidebar.js` ada toggle `sidebar-collapsed` |
| 2 | Periode kurikulum 5 tahun | ✅ DONE | memory + `routes/periode.py`; inklusif (mulai+4) |
| 3 | Reorg menu: matriks→Plan, Do=RPS, assessment→Check | ✅ DONE | `sidebar.js` PLAN berisi semua matriks+pemetaan; DO hanya RPS; CHECK berisi penilaian/rumusan/nilai/laporan |
| 4 | Aksi validasi/lock di semua modul | ✅ DONE (perlu audit cakupan) | `services/lock_guard.py` dipakai di `master_mk`, dll. (commit `2e005b7`: "lock guard semua master") |
| 5 | Data master jenis MK & kategori PL | ✅ DONE | `models/master_dropdown.py` + `/api/jenis-mk` & `/api/kategori-pl`; form pakai `remote-select` |
| 6 | Pemenuhan CPL otomatis | ✅ DONE | `routes/peta_cpl.py` derive dari `mapping_cpl_mk` × semester MK |
| 7 | Pemetaan CPL-BK-MK otomatis (data) | ✅ DONE | `routes/pemetaan_cpl_bk_mk.py` derive dari `cpl_bk` ∧ `bk_mk` |
| 8 | Modul dokumen/notulensi (upload PDF) | ✅ DONE | "Agenda & Dokumen Mutu" (`log_peninjauan`, Supabase Storage) |
| 9 | Multi-role RBAC + akses dibuka penuh dulu | ✅ DONE | 6 role di `permission.py`; `OPEN_ACCESS=true` (config.py:212) |
| 10 | Peta referensi per fitur (3 sumber) | ✅ DONE & **terverifikasi akurat** | `referensi_page.js`; nomor halaman sudah dicek ke PDF (lihat §1.4) |
| 11 | Cetak RPS | 🟡 PARTIAL | tombol `window.print()` ada; **belum** ada CSS `@media print` sesuai template buku |
| **12** | **Kolom referensi 3 sumber MELEKAT di tiap baris data** | ❌ **GAP (prioritas #1)** | Baru 1 kolom `referensi` tunggal di cpl/bk; PL/MK/CPMK belum punya |
| 13 | Visual pemetaan CPL-BK-MK gaya buku (MK tengah, BK atas, CPL kode) | ❌ GAP | Saat ini tabel biasa, bukan diagram |
| 14 | Organisasi MK "ke samping" (kode,nama,kompetensi,BKMK,semester horizontal) | 🟡 VERIFIKASI | perlu cek `organisasi_page.js` |
| 15 | Matriks CPL-PL: kotak CPL kelebar | ❌ BUG | lihat BUG-2 |
| 16 | Export Excel peta referensi per fitur | ❌ GAP (permintaan tambahan klien) | belum ada tombol export |

**Kesimpulan:** fokus revisi = **(A) kolom referensi 3 sumber per data**, **(B) visual sesuai buku**, **(C) cetak RPS template**, **(D) sapu bug migrasi & korektif**. Sisanya verifikasi + polish.

---

## 1. ATURAN EKSEKUSI (WAJIB DIPATUHI)

### 1.1 Perintah verifikasi (jalankan sebelum & sesudah tiap tugas)
```bash
# Sintaks Python
python -m py_compile config.py app.py routes/*.py models/*.py services/*.py db/*.py middleware/*.py
# Unit test (baseline saat ini: 14 passed)
python -m pytest tests/ -q
# Smoke test DB sqlite bersih (TANPA merusak DB dev)
rm -f _coba.db && DATABASE_URI="sqlite:///_coba.db" python -c "import app; a=app.create_app(); print('boot OK')" ; rm -f _coba.db
# Sintaks JS bila ada node
node --check static/js/<file>.js
```
**Pantang commit bila `py_compile` atau `pytest` gagal.**

### 1.2 Fakta teknis yang kalau dilanggar → fitur rusak senyap
1. **Vercel filesystem read-only & ephemeral** → semua upload PDF lewat **Supabase Storage** (`services/storage_service.py`), jangan ke `uploads/` di prod.
2. **`create_all()` tidak menambah KOLOM** ke tabel lama → kolom baru WAJIB didaftarkan di `_NEW_COLUMNS` pada `db/migrate.py` (`ensure_columns()`, idempotent). Ini pusat dari BUG-1.
3. **Postgres ≠ MySQL** → tak ada `YEAR`/`AUTO_INCREMENT`; jangan jalankan SQL baseline MySQL mentah ke Supabase.
4. **Action permission harus terdaftar** di `services/permission.py`, kalau tidak semua user kena 403 (mode OPEN_ACCESS menutupi ini, tapi tetap jaga konsistensi).
5. **`to_dict()` mengembalikan SEMUA kolom termasuk `password_hash`** → jangan kirim objek User mentah; pakai payload aman.
6. **Periode 5 tahun inklusif**: `tahun_selesai = tahun_mulai + 4`.

### 1.3 Aturan git (khusus proyek ini)
- Commit **per tugas**, pesan Bahasa Indonesia yang jelas.
- **JANGAN tambah trailer `Co-Authored-By`** (Vercel Hobby memblokir deploy repo privat bila ada co-author) — ini aturan deploy yang sudah ditetapkan pemilik repo; minta konfirmasi sebelum commit.
- Author commit = email pemilik repo. Push ke `main` (Vercel auto-deploy).

### 1.4 Verifikasi rujukan tabel ke sumber (SUDAH DIKERJAKAN — hasil)
Klien menekankan tiap fitur harus punya rujukan jelas; teman Anda minta cek ulang ambiguitas "hal 24". **Sudah diverifikasi langsung ke PDF buku:**
- Offset PDF↔halaman cetak buku **konsisten +13** (Tabel 8 di PDF hlm 37 = cetak **hal 24**; Tabel 14 di PDF hlm 46 = cetak **hal 33**).
- **Tabel 7 (Pemetaan CPL-MK) dan Tabel 8 (Pemetaan BK-CPL-MK) memang berada di halaman cetak yang SAMA (24)** — itu sebabnya gambar lama seakan "dobel hal 24".
- `referensi_page.js` **sudah benar**: Pemetaan CPL-BK-MK→Tabel 8 (hal 24), Matriks CPMK-MK→Tabel 14 (hal 33). Seluruh 16 nomor halaman lain juga dicek cocok (offset +13). → **Tidak perlu perubahan; cukup dicatat sebagai "verified".**

---

## 2. RENCANA PER MODUL (dengan prioritas)

Legenda prioritas: **P0** = blokir/ditekankan klien · **P1** = daftar tertulis & transkrip · **P2** = penting tapi tidak memblokir · **P3** = polish/verifikasi.

### MODUL 1 — Fondasi Referensi 3 Sumber & Migrasi  **[P0]**
**Tujuan:** setiap data master punya 3 kolom referensi yang melekat: `ref_buku` (buku panduan: tabel/hal), `ref_spreadsheet` (sheet rancangan), `ref_pikobe` (ledik/tabel no).
**Tugas:**
1. Model: tambah `ref_buku`, `ref_spreadsheet`, `ref_pikobe` (TEXT) ke `ProfilLulusan`, `CPLProdi`, `BahanKajian`, `MataKuliah`, `CPMK`. Pertahankan kolom `referensi` lama (migrasi nilai → `ref_buku`).
2. `db/migrate.py`: daftarkan SEMUA kolom baru di `_NEW_COLUMNS` (+ perbaikan BUG-1 sekalian: `profil_lulusan.referensi`, `profil_lulusan.kategori`, `mata_kuliah.jenis/is_capstone/prasyarat/deskripsi_singkat`).
3. Routes master (`master_pl/cpl/bk/mk/cpmk`): terima & simpan 3 field; sertakan di `to_dict`/response.
4. Frontend `master_data.js` + `form_builder.js`: 3 input referensi per form; tampilkan 3 kolom di tabel (boleh ringkas/tooltip).
**Acuan buku:** Tabel 1 (hal 15), Tabel 2 (hal 17), Tabel 4 (hal 19–20) yang memang bawa kolom Referensi.
**Selesai bila:** tambah PL/CPL/BK/MK/CPMK dengan 3 referensi → tersimpan, tampil, dan bertahan setelah `ensure_columns()` di DB lama.

### MODUL 2 — Master Data & Data Master Dropdown  **[P1]**
**Status:** CRUD + dropdown jenis/kategori sudah jalan.
**Tugas:**
1. Audit konsistensi: pertimbangkan hapus `fallback:"text"` pada `remote-select` jenis MK/kategori PL agar tidak bisa input bebas (cegah "MKDU" vs "Mata Kuliah Bersama Universitas"). Atau normalisasi saat simpan.
2. Tambah UI kelola isi data master (CRUD daftar jenis MK & kategori PL) bila belum ada halaman pengelolanya.
3. MK: pastikan field `jenis` divalidasi terhadap master (bukan sekadar default "wajib").
**Acuan:** Tabel 9 (hal 26–27) untuk MK + kolom "jenis".
**Selesai bila:** menambah jenis baru hanya lewat data master; form MK memanggilnya; tak ada string bebas yang lolos.

### MODUL 3 — Matriks & Pemetaan  **[P1]**
**Status:** matriks CPL-PL/CPL-BK/BK-MK/CPL-MK/CPMK-MK + pemetaan CPL-BK-MK otomatis sudah ada di PLAN.
**Tugas:**
1. **Visual pemetaan CPL-BK-MK gaya buku (Tabel 8, hal 24):** render diagram **MK di tengah, BK di atas, CPL sebagai kode** — bukan tabel datar. (komponen baru, mis. `pemetaan_visual.js` atau perluas `matrix_grid`/`spider_chart`).
2. **Penyamaan input tabel pemetaan**: samakan kolom/format input semua tabel pemetaan agar konsisten dgn panduan (Tabel 3/5/6/7/8/12/14/15).
3. Perbaiki **BUG-2** (kotak CPL kelebar) pada matriks CPL-PL.
**Acuan:** Tabel 3 (18), 5 (21), 6 (22), 7 (24), 8 (24), 12 (31), 14 (33), 15 (35).
**Selesai bila:** pemetaan CPL-BK-MK tampil sebagai diagram berkode mirip buku; semua tabel pemetaan seragam; matriks CPL-PL rapi.

### MODUL 4 — Organisasi MK & Peta Pemenuhan CPL  **[P1/P2]**
**Status:** Peta Pemenuhan CPL sudah otomatis ✅.
**Tugas:**
1. Verifikasi **Organisasi MK ditata "ke samping"**: kolom kode, nama, kompetensi, BK-MK, dan **semester memanjang horizontal** (Tabel 10, hal 29). Perbaiki bila masih vertikal.
2. Tampilkan organisasi **per semester** (Semester 1..8) dengan bentuk kode.
3. Filter periode pada peta CPL & organisasi (lihat BUG-4) agar tak mencampur antar-periode.
**Selesai bila:** layout horizontal sesuai buku; angka pemenuhan murni dari relasi (tanpa input manual).

### MODUL 5 — RPS (DO)  **[P1]**
**Status:** model RPS + mingguan + input ada; print masih `window.print()` polos.
**Tugas:**
1. **CSS `@media print`** + layout cetak yang **persis template buku (Bab 4, hal 42–45)** & contoh RPS di spreadsheet: identitas MK, kode, dosen pengampu, deskripsi, CPMK/Sub-CPMK + pemetaannya, tabel mingguan dengan Sub-CPMK terkait, bobot, pustaka.
2. Pastikan data CPMK/Sub-CPMK per minggu ikut tercetak.
3. (Opsional) export PDF server-side bila print browser kurang rapi.
**Acuan:** Buku hal 42–45; Sheet "Rancangan RPS" & "Contoh RPS".
**Selesai bila:** klik Cetak → hasil sesuai bentuk template (ini PR utama yang klien sebut).

### MODUL 6 — CHECK (Penilaian, Rumusan, Nilai, Laporan)  **[P2]**
**Status:** penilaian/bobot, rumusan MK/CPL, input nilai, laporan CPL + laporan mahasiswa sudah ada (seed demo agar tak 0).
**Tugas:**
1. Lengkapi kolom referensi sumber untuk fitur CHECK (di review masih kosong) — minimal di `referensi_page.js`.
2. Verifikasi rumusan akhir MK & CPL sesuai Tabel 18a (hal 75) & Tabel 20 (hal 78).
3. Uji end-to-end: input nilai → rumusan MK → rumusan CPL → laporan (staf) → laporan mahasiswa (self).
**Selesai bila:** alur nilai→laporan konsisten & mahasiswa melihat hasilnya.

### MODUL 7 — ACTION (Agenda & Dokumen Mutu / Log Peninjauan)  **[P3 — mostly done]**
**Tugas:** verifikasi upload multi-PDF ke Supabase Storage di prod; pastikan jenis agenda (peninjauan_kurikulum/reuni_alumni/fgd_lokakarya/rapat_mutu) + notulensi tersimpan; tambah referensi sumber bila relevan.

### MODUL 8 — RBAC & Administrasi  **[P3 — mostly done]**
**Tugas:** OPEN_ACCESS tetap `true` (sesuai keputusan "buka dulu"); pastikan struktur 6 role utuh untuk pengetatan nanti; verifikasi Manajemen Pengguna tidak membocorkan `password_hash` (lihat BUG-3).

### MODUL 9 — Referensi & Export  **[P2]**
**Status:** halaman peta referensi per fitur sudah ada & akurat.
**Tugas:**
1. Tombol **Export Excel** peta referensi (permintaan klien) — generate .xlsx dari `REF_DATA` (boleh server-side via `openpyxl` atau client-side).
2. Tautkan tiap baris peta ke halaman fiturnya.
**Selesai bila:** klien bisa unduh spreadsheet pemetaan referensi untuk diperiksa & diberi feedback.

### MODUL 10 — UI/UX Global  **[P3]**
**Tugas:** uji sidebar collapsible di mobile; rapikan lebar kolom tabel master yang kini bertambah karena 3 kolom referensi (gunakan tooltip/expand); konsistensi tombol Validasi/Lock + status terkunci terlihat jelas di tiap modul.

---

## 3. RENCANA PERBAIKAN BUG

| ID | Prioritas | Bug | Bukti | Perbaikan |
|----|-----------|-----|-------|-----------|
| **BUG-1** | **P0** | Migrasi kolom tak lengkap: `profil_lulusan.referensi` & `profil_lulusan.kategori`, `mata_kuliah.jenis/is_capstone/prasyarat/deskripsi_singkat` ADA di model tapi TIDAK di `_NEW_COLUMNS`. Di Supabase DB lama → error "column does not exist". | `db/migrate.py:15-30` vs `models/profil_lulusan.py`, `models/mata_kuliah.py` | Tambahkan semua kolom tsb ke `_NEW_COLUMNS`; jalankan `?init=1`/`ensure_columns()`; verifikasi di DB lama. |
| **BUG-2** | P1 | Matriks CPL-PL: kotak kolom CPL terlalu lebar (seakan ada deskripsi padahal kosong). | review klien; `static/css/matrix.css` + `matrix_page.js` | Set lebar tetap/auto kolom CPL; jangan render kolom deskripsi kosong. |
| **BUG-3** | P1 | Potensi kebocoran `password_hash` via `to_dict()` di endpoint user. | `models/user.py` + `routes/users.py` | Pastikan response user pakai payload aman (whitelist field), bukan `to_dict()` mentah. |
| **BUG-4** | P2 | `peta_cpl` & `pemetaan_cpl_bk_mk` query SEMUA CPL/MK **tanpa filter `periode_id`** → bila >1 periode, data tercampur. | `routes/peta_cpl.py:19-21`, `routes/pemetaan_cpl_bk_mk.py:19-21` | Filter by periode aktif (konsisten dgn fix `periode_id hardcoded` commit `2e005b7`). |
| **BUG-5** | P2 | `remote-select` jenis MK/kategori PL punya `fallback:"text"` → input bebas masih bisa lolos → inkonsistensi data yang justru ingin dicegah. | `static/js/pages/master_data.js:16,19` | Hapus fallback atau normalisasi server-side terhadap master. |
| **BUG-6** | P3 | Cakupan lock guard: pastikan SEMUA route tulis (matrix toggle, rps, penilaian, dokumen) memanggil `assert_periode_unlocked`, bukan hanya master. | `services/lock_guard.py` pemakaian | Audit & tambal yang terlewat. |

> Catatan: BUG-4/5/6 = korektif preventif; pada deployment 1 periode aktif, dampak BUG-4 belum terasa tapi wajib dibereskan sebelum periode ke-2.

---

## 4. URUTAN EKSEKUSI (SPRINT)

**Sprint 1 — Pondasi & bug kritis [P0]** (kerjakan dulu, saling bergantung):
1. BUG-1 (lengkapi `_NEW_COLUMNS`).
2. MODUL 1 (kolom referensi 3 sumber: model → migrate → routes → UI).
→ Verifikasi: pytest hijau + smoke test + CRUD 3 referensi bertahan.

**Sprint 2 — Sesuai panduan visual & template [P1]:**
3. MODUL 5 (cetak RPS template).
4. MODUL 3 (visual pemetaan CPL-BK-MK + penyamaan input + BUG-2).
5. MODUL 4 (organisasi MK horizontal + BUG-4).
6. BUG-3.

**Sprint 3 — Kelengkapan & polish [P2/P3]:**
7. MODUL 9 (export Excel referensi).
8. MODUL 2 (konsistensi dropdown + BUG-5), MODUL 6 (verifikasi alur nilai), BUG-6.
9. MODUL 7/8/10 (verifikasi + polish UI).

---

## 5. PROTOKOL "SELESAI" (Definition of Done) per tugas
1. `py_compile` & `pytest` hijau (jangan turunkan dari 14 test; tambah test untuk logika baru).
2. Smoke test boot DB bersih sukses.
3. Bukti fungsional nyata (klik UI / panggil API) — bukan sekadar file ada.
4. Migrasi kolom baru terdaftar di `_NEW_COLUMNS` & teruji di DB lama.
5. Commit Bahasa Indonesia, tanpa trailer co-author, author = pemilik repo.

---

### Lampiran A — Peta rujukan tabel (terverifikasi PDF, offset +13)
PL→T1(h15) · CPL→T2(h17) · BK→T4(h19-20) · MK→T9(h26-27) · CPMK→T12(h31) · Matriks CPL-PL→T3(h18) · CPL-BK→T5(h21) · BK-MK→T6(h22) · CPL-MK→T7(h24) · CPMK-MK→T14(h33) · Pemetaan CPL-BK-MK→T8(h24) · Organisasi MK→T10(h29) · Pemenuhan CPL→T11(h30) · MK-CPMK-SubCPMK→T15(h35) · RPS→Bab4(h42-45).
