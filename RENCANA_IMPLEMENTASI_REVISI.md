# RENCANA IMPLEMENTASI REVISI — Sistem Kurikulum OBE
> Dokumen ini untuk **agen pelaksana**. Kerjakan **BERURUTAN (SEQUENTIAL)**, satu langkah selesai + diverifikasi, baru lanjut. **JANGAN kerja paralel.** Jangan berasumsi — kalau ragu, baca file sumber yang disebут.

---

## 0. WAJIB DIBACA DULU (konteks & aturan main)

### 0.1 Target proyek
- Aplikasi = **Flask + SQLAlchemy** (Python). Bukan PHP/MySQL murni. File SQL (`sistem_kurikulum_obe (2).sql`) hanya **referensi DATA & skema**, bukan aplikasi yang dijalankan.
- Path proyek: `C:\Romadhon Data penting\Downloads\YT DON\Kurikulum OBE`
- DB: **Supabase/PostgreSQL** (produksi, via env `DATABASE_URL`) atau **SQLite** (lokal default). Hosting: **Vercel** (serverless).
- Frontend: **vanilla JS** (tanpa React/Vue). Pola: dispatch-table di `static/js/core/router.js` & `static/js/components/sidebar.js`.
- Komentar kode pakai Bahasa Indonesia (ikuti gaya yang ada).

### 0.2 Cara menjalankan & verifikasi (HAFALKAN — dipakai tiap langkah)
```bash
# 1. Cek sintaks semua Python sebelum & sesudah ngoding:
python -m py_compile config.py app.py routes/*.py models/*.py services/*.py db/*.py middleware/*.py

# 2. Jalankan unit test:
python -m pytest tests/ -q

# 3. Smoke test pakai DB sqlite bersih (TANPA merusak DB dev):
rm -f _coba.db
DATABASE_URI="sqlite:///_coba.db" python -c "import app; a=app.create_app(); app.seed_all(); print('OK boot & seed')"
rm -f _coba.db

# 4. Cek sintaks JS (kalau ada node):
node --check static/js/components/sidebar.js
```
**ATURAN: jangan pernah commit kalau `py_compile` atau `pytest` gagal.**

### 0.3 Aturan git
- Commit **per langkah** (R1 selesai → commit, R2 selesai → commit, dst). Pesan commit jelas, Bahasa Indonesia.
- **JANGAN tambahkan trailer `Co-Authored-By`** di pesan commit (Vercel Hobby memblokir deploy kalau ada co-author di repo privat).
- Author commit harus email pemilik repo (`romadhonardiansyah1@gmail.com`). Cek: `git config user.email`.
- Push ke `main` (Vercel auto-deploy dari main). Kalau push ke main diblokir, minta izin pemilik.

### 0.4 FAKTA TEKNIS PENTING (kalau dilanggar → fitur rusak senyap)
1. **Filesystem Vercel itu read-only & sementara.** File yang di-`save()` ke disk akan HILANG setelah cold start. → Semua upload PDF WAJIB lewat **Supabase Storage** (lihat `services/storage_service.py`). Jangan simpan ke `uploads/` di produksi.
2. **`create_all()` (SQLAlchemy) hanya membuat TABEL baru, TIDAK menambah KOLOM baru** ke tabel yang sudah ada di Supabase. Untuk kolom baru, pakai `ensure_columns()` di `db/migrate.py` (idempotent). 
3. **PostgreSQL ≠ MySQL.** Di SQL baseline ada tipe `YEAR`, `BOOLEAN`, `AUTO_INCREMENT` (MySQL). Di Postgres: `YEAR` TIDAK ADA → pakai `INTEGER`. Jangan jalankan SQL baseline mentah ke Supabase.
4. **Permission action string harus terdaftar.** Kalau sebuah route minta action yang tidak ada di `services/permission.py`, semua user kena 403 (ini bug lama: `manage_log`). Dengan mode **OPEN ACCESS** (lihat R3) masalah ini hilang, tapi tetap jaga konsistensi.
5. **`to_dict()` mengembalikan SEMUA kolom termasuk `password_hash`.** Jangan kirim object User mentah ke frontend; pakai payload aman (lihat `routes/auth.py`).
6. **Periode 5 tahun = inklusif**, jadi `tahun_selesai = tahun_mulai + 4` (mis. 2024–2028), BUKAN +5. Hati-hati off-by-one.

### 0.5 Keadaan repo saat ini (CEK DULU sebelum bikin baru — banyak yang MUNGKIN sudah ada)
Repo ini sudah pernah direvisi sebelumnya. Kemungkinan besar SUDAH ADA:
- Periode 5 tahun (`routes/periode.py`, `db/seed.py`), role 6 buah + gating ketat (`services/permission.py`), modul "Agenda & Dokumen Mutu" (`models/log_peninjauan.py`, `routes/log_peninjauan.py`, `static/js/pages/agenda_page.js`), Supabase Storage (`services/storage_service.py`), akun mahasiswa + nilai demo (`db/seed_rps.py`, `db/seed_penilaian.py`).

**Maka tugas utamamu BUKAN bikin dari nol, tapi: (a) UBAH akses jadi TERBUKA (open access), (b) VERIFIKASI 3 revisi wajib, (c) kerjakan perbaikan Sprint Review.** Untuk tiap langkah: **CEK dulu apakah sudah ada → kalau ada, sesuaikan; kalau belum, buat sesuai spec di sini.**

---

# BAGIAN 1 — REVISI WAJIB (prioritas tertinggi)

## R1. Periode kurikulum = 5 TAHUN

**Tujuan:** setiap periode kurikulum berdurasi tepat 5 tahun (mis. 2024–2028, 2029–2033), dan dokumen terpisah per periode.

**Langkah:**
1. Buka `config.py`, pastikan ada:
   ```python
   PERIODE_DURATION_YEARS = 5
   ```
2. Buka `routes/periode.py`. Pastikan `create_periode()` MEMAKSA `tahun_selesai = tahun_mulai + 4`. Kode yang benar:
   ```python
   def _span():
       return config.PERIODE_DURATION_YEARS - 1  # 5 tahun inklusif → selisih 4

   def create_periode():
       data = request.get_json(silent=True) or {}
       tahun_mulai = int(data["tahun_mulai"])
       tahun_selesai = tahun_mulai + _span()          # SELALU 5 tahun
       nama = data.get("nama") or ("Kurikulum " + str(tahun_mulai) + "-" + str(tahun_selesai))
       periode = PeriodeKurikulum(prodi_id=data["prodi_id"], nama=nama,
           tahun_mulai=tahun_mulai, tahun_selesai=tahun_selesai,
           status=data.get("status", "draft"))
       state.db.add(periode); state.db.commit()
       return created(data=periode.to_dict())
   ```
   `update_periode()` juga harus menjaga: `periode.tahun_selesai = int(periode.tahun_mulai) + _span()` setiap kali `tahun_mulai` diubah. (Butuh `import config` di atas file.)
3. Buka `db/seed.py` fungsi `seed_periode()`. Pastikan men-seed minimal 2 periode 5-tahunan, contoh: `2024–2028` (status `aktif`) dan `2029–2033` (status `draft`). Kembalikan id periode aktif.
4. **Frontend:** dropdown periode ada di `static/js/components/header.js` (`#periode-dropdown`). Pastikan label tampil `Kurikulum 2024-2028` dst.

**Verifikasi R1:**
```bash
DATABASE_URI="sqlite:///_c.db" python -c "
import app, state
app.create_app(); app.seed_all()
from models.period import PeriodeKurikulum
for p in state.db.query(PeriodeKurikulum).all():
    print(p.nama, p.tahun_mulai, '-', p.tahun_selesai, '| span=', p.tahun_selesai-p.tahun_mulai, '(harus 4)')
"; rm -f _c.db
```
Output tiap periode harus `span= 4`. **Commit:** `git commit -am "R1: pastikan periode kurikulum 5 tahun"`

---

## R2. Modul Dokumen & Notulensi (REUNI ALUMNI) — upload PDF

**Tujuan klien:** tempat mengumpulkan dokumen + notulensi saat **reuni alumni** (dan kegiatan mutu lain). Minimal upload **PDF**.

**Desain (sudah ada di repo, VERIFIKASI; kalau belum, buat persis ini):**
- Model `models/log_peninjauan.py` → `LogPeninjauan` punya kolom: `jenis` (string), `periode_id` (FK nullable), `judul`, `tanggal` (Date), `lokasi`, `peserta` (Text), `catatan` (Text = **notulensi**), `status`. Relasi `dokumen_list` → `DokumenBukti`.
- `DokumenBukti`: `log_id`, `filename`, `filepath`, `storage_key`, `storage_backend` (`local`|`supabase`), `ukuran`.
- `config.py` punya:
  ```python
  JENIS_AGENDA = ("peninjauan_kurikulum", "reuni_alumni", "fgd_lokakarya", "rapat_mutu")
  JENIS_AGENDA_LABELS = {"peninjauan_kurikulum":"Peninjauan Kurikulum","reuni_alumni":"Reuni Alumni","fgd_lokakarya":"FGD / Lokakarya","rapat_mutu":"Rapat Mutu"}
  ALLOWED_EXTENSIONS = {"pdf"}            # HANYA pdf
  MAX_UPLOAD_SIZE_MB = 10
  SUPABASE_URL = os.environ.get("SUPABASE_URL","")
  SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", os.environ.get("SUPABASE_KEY",""))
  SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET","obe-dokumen")
  ```
- `services/storage_service.py`: fungsi `save_pdf(file_storage, folder)`, `signed_url(key)`, `delete_file(doc)`. Kalau env Supabase ada → simpan ke Supabase Storage; kalau tidak → simpan ke disk lokal (`uploads/`) sebagai fallback dev. **Validasi PDF-only & batas ukuran ada di sini.**
- `routes/log_peninjauan.py`: endpoint list (filter `?jenis=` & `?periode_id=`), create, update, get (with dokumen), delete, `POST /api/log-peninjauan/<id>/upload` (MULTIPLE pdf), `GET /api/dokumen-bukti/<id>/download`, `DELETE /api/dokumen-bukti/<id>`.
- Frontend `static/js/pages/agenda_page.js`: daftar agenda + filter jenis, form (jenis dropdown, judul, tanggal, lokasi, peserta, **notulensi**), drag-and-drop multi-PDF, daftar lampiran + unduh/hapus. Terdaftar di `router.js` (`agenda`) & sidebar.

**Kalau modul ini BELUM ada**, buat persis spec di atas. Pola upload (penting, drag-drop pakai `FormData` + `fetch`, bukan `Api` JSON):
```javascript
function _upload(id, fileList){
  var fd=new FormData();
  for(var i=0;i<fileList.length;i++){ if(/\.pdf$/i.test(fileList[i].name)) fd.append("files", fileList[i]); }
  fetch("/api/log-peninjauan/"+id+"/upload",{method:"POST",credentials:"same-origin",body:fd})
    .then(r=>r.json()).then(res=>{ ToastComponent.success((res.data&&res.data.count||0)+" file terunggah"); _openDetail(id); });
}
```

**Supabase Storage (MANUAL, di luar kode — wajib biar upload jalan di produksi):**
1. Supabase Dashboard → **Storage → New bucket** → nama `obe-dokumen`, **Public OFF**.
2. Vercel env: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` (service_role key), `SUPABASE_BUCKET=obe-dokumen`.

**Verifikasi R2 (fallback lokal, tanpa Supabase):**
```bash
DATABASE_URI="sqlite:///_c.db" python -c "
import app, state
from datetime import date
from io import BytesIO
from werkzeug.datastructures import FileStorage
app.create_app(); app.seed_all()
from models.log_peninjauan import LogPeninjauan, DokumenBukti
from services import storage_service
log=LogPeninjauan(jenis='reuni_alumni', judul='Reuni Alumni 2026', tanggal=date(2026,6,1), lokasi='Aula', peserta='Alumni', catatan='Notulensi reuni...', status='final')
state.db.add(log); state.db.commit()
meta=storage_service.save_pdf(FileStorage(stream=BytesIO(b'%PDF-1.4 x'),filename='notulen.pdf',content_type='application/pdf'),'agenda/'+str(log.id))
print('upload backend=',meta['storage_backend'],'key=',meta['storage_key'])
try:
    storage_service.save_pdf(FileStorage(stream=BytesIO(b'x'),filename='jahat.exe'),'agenda/1'); print('BUG: non-pdf lolos')
except ValueError as e: print('non-pdf ditolak OK')
"; rm -f _c.db; rm -rf uploads/agenda
```
Harus: ada `jenis='reuni_alumni'`, upload sukses, non-PDF DITOLAK. **Commit:** `git commit -am "R2: verifikasi modul dokumen & notulensi reuni (upload PDF)"`

---

## R3. Tambah ROLE + AKSES TERBUKA (open access)  ← PALING PENTING & PALING BEDA DARI KODE SEKARANG

**Permintaan klien:** ada role **kaprodi, tim_kurikulum, dosen, mahasiswa** (boleh + admin_universitas, dekan) DI DATABASE, **tapi untuk sekarang AKSES DIBUKA SEMUA — semua role bisa mengakses semua fitur.** (Sesuai dokumen visi: "fitur dibangun terbuka dulu, role-mapping di akhir".)

> ⚠️ Kode saat ini memakai **gating ketat** (tiap menu/endpoint dibatasi per role → banyak 403). Kamu harus **MEMATIKAN gating itu** dengan flag `OPEN_ACCESS=True`, **tanpa menghapus** struktur role (biar gampang dinyalakan lagi nanti).

### R3.1 Tambah flag di `config.py`
Tambahkan (di dekat bagian Role):
```python
# Akses terbuka: bila True, SEMUA user terautentikasi bisa akses SEMUA fitur.
# Role tetap disimpan di DB untuk pembatasan di masa depan.
OPEN_ACCESS = os.environ.get("OPEN_ACCESS", "true").lower() == "true"
```
Pastikan `ROLES` memuat minimal 4 role yang diminta klien:
```python
ROLES = ("admin_universitas", "dekan", "kaprodi", "tim_kurikulum", "dosen", "mahasiswa")
ROLE_LABELS = {"admin_universitas":"Admin Universitas","dekan":"Dekan / Fakultas","kaprodi":"Kaprodi","tim_kurikulum":"Tim Kurikulum","dosen":"Dosen / DPA","mahasiswa":"Mahasiswa"}
```

### R3.2 Matikan gating di backend — `middleware/role_guard.py`
Ganti seluruh isi file dengan:
```python
"""
Decorator otorisasi berbasis role.
Bila config.OPEN_ACCESS True, cukup butuh login (semua action diizinkan).
"""
from functools import wraps
from flask import jsonify
import config
import state
from services.permission import check_permission


def require_action(action):
    def decorator(handler):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            user = state.current_user
            if user is None:
                return jsonify({"error": "Autentikasi diperlukan"}), 401
            # MODE OPEN ACCESS: semua user login boleh akses semua fitur.
            if getattr(config, "OPEN_ACCESS", False):
                return handler(*args, **kwargs)
            if not check_permission(user.role, action):
                return jsonify({"error": "Akses ditolak", "required_action": action}), 403
            return handler(*args, **kwargs)
        return wrapper
    return decorator
```

### R3.3 Kirim flag ke frontend — `routes/auth.py`
Di fungsi `_build_session_payload(user_dict)`, tambahkan agar frontend tahu mode terbuka & menampilkan semua menu:
```python
import config
from services.permission import get_allowed_actions, get_scope, get_all_roles, ROLE_ACTIONS
# ... di dalam _build_session_payload, sebelum return:
payload["open_access"] = getattr(config, "OPEN_ACCESS", False)
if payload["open_access"]:
    # gabungkan SEMUA action yang dikenal sistem → sidebar tampilkan semua menu
    semua = set()
    for r in ROLE_ACTIONS.values():
        semua |= set(r["allowed"])
    payload["allowed_actions"] = sorted(semua)
```
(Pastikan `password_hash` TIDAK ikut di payload — sudah dibuang di kode existing; jangan diubah.)

### R3.4 Frontend tampilkan semua menu — `static/js/components/sidebar.js`
Ubah fungsi `init` & `_allows` agar saat `open_access` semua item tampil. Cari `function init(role, allowedActions)` dan ganti dua fungsi berikut:
```javascript
function _allows(allowedActions, action) {
    if (!action) return true;
    if (AppState.user && AppState.user.open_access) return true;   // OPEN ACCESS → tampilkan semua
    if (!allowedActions) return false;
    return allowedActions.indexOf(action) !== -1;
}

function init(role, allowedActions) {
    var container = document.getElementById("sidebar-menu");
    container.innerHTML = "";
    var openAccess = AppState.user && AppState.user.open_access;
    if (openAccess || _allows(allowedActions, "view_kurikulum")) {
        var dashItem = _createItem({ key: "dashboard", label: "Dashboard", action: null });
        dashItem.style.marginBottom = "4px";
        container.appendChild(dashItem);
    }
    // ... sisanya (loop MENU_STRUCTURE) BIARKAN sama; _allows sudah menangani open access.
    for (var s = 0; s < MENU_STRUCTURE.length; s++) { /* kode loop existing */ }
}
```
(Cukup ubah `_allows` + baris Dashboard. Loop section existing tidak perlu diubah karena `_allows` sudah return true saat open access.)

### R3.5 Seed akun demo per role — `db/seed_rps.py` / `app.py seed_all`
Pastikan ada akun login untuk tiap role yang diminta. Tambahkan helper di `app.py` `seed_all()` SETELAH user admin dibuat:
```python
from services.auth_service import hash_password
demo = [("kaprodi","kaprodi","Kaprodi Demo","kaprodi"),
        ("timkurikulum","timkurikulum","Tim Kurikulum Demo","tim_kurikulum"),
        ("dosen","dosen","Dosen Demo","dosen")]
for uname, pw, nama, role in demo:
    if session.query(User).filter_by(username=uname).first() is None:
        session.add(User(username=uname, password_hash=hash_password(pw), nama=nama, email=uname+"@prodi.ac.id", role=role))
session.commit()
```
(Akun mahasiswa `2024001..2024005` sudah dibuat `seed_mahasiswa`. `admin` = role kaprodi.)

**Verifikasi R3 (PALING PENTING):**
```bash
DATABASE_URI="sqlite:///_c.db" python -c "
import app
a=app.create_app(); app.seed_all(); c=a.test_client()
def login(u,p): return c.post('/api/auth/login',json={'username':u,'password':p}).get_json()
r=login('2024001','2024001')  # mahasiswa
print('open_access flag:', r['data'].get('open_access'), '(harus True)')
print('mahasiswa GET /api/pl :', c.get('/api/pl').status_code, '(harus 200, BUKAN 403)')
print('mahasiswa GET /api/users :', c.get('/api/users').status_code, '(harus 200 krn open access)')
print('mahasiswa POST agenda :', c.post('/api/log-peninjauan',json={'judul':'x','tanggal':'2026-01-01'}).status_code, '(harus 201)')
"; rm -f _c.db
```
Semua harus 200/201 (TIDAK boleh 403). **Commit:** `git commit -am "R3: tambah role + mode akses terbuka (open access) untuk semua user"`

---

# BAGIAN 2 — PERBAIKAN DARI SPRINT REVIEW (permintaan Bu Endang)
> Sumber: `Beberapa hal yang perlu diperbaiki...pdf` + transkrip `Sprint Review (1).pdf`. Kerjakan setelah Bagian 1. Urut sesuai dampak.

## T1. Sidebar bisa dibuka-tutup (collapsible)
**Di `templates/app.html`**: tambah tombol toggle di dalam `.sidebar-brand` atau header:
```html
<button id="sidebar-toggle" class="btn btn-sm btn-outline" title="Buka/Tutup menu">☰</button>
```
**Di `static/js/components/sidebar.js`** (akhir IIFE, dalam `init` atau `DOMContentLoaded`):
```javascript
var t=document.getElementById("sidebar-toggle");
if(t) t.addEventListener("click",function(){ document.querySelector(".app-layout").classList.toggle("sidebar-collapsed"); });
```
**Di `static/css/layout.css`**: saat `.app-layout.sidebar-collapsed .sidebar{ width:0; overflow:hidden; }` (atau width kecil ikon-only). Uji: klik tombol → sidebar menyempit/menghilang, klik lagi → muncul.

## T2. Reorganisasi sidebar: Matriks & Pemetaan → PLAN; DO = RPS saja
Klien tegas: **semua matriks & pemetaan masuk PLAN**, **DO isinya RPS saja**, assessment tetap CHECK.
Di `static/js/components/sidebar.js` ubah `MENU_STRUCTURE`: pindahkan item `matrix-*`, `pemetaan-cpl-bk-mk`, `organisasi-mk`, `peta-cpl`, `mk-subcpmk` dari section `DO` ke section `PLAN` (taruh setelah `master-cpmk`). Section `DO` HANYA berisi:
```javascript
{ section: "DO", items: [ { key: "rps", label: "RPS", action: "view_kurikulum" } ] },
```
(Item lain & key tidak berubah; `router.js` tetap sama.) Uji: menu PLAN berisi master+matriks+pemetaan, DO cuma RPS.

## T3. Kategori PL & Jenis MK jadi DATA MASTER (dropdown, bukan ketik bebas)
Klien: biar database konsisten (mis. "MKDU" vs "Mata Kuliah Bersama Universitas" jangan dianggap beda).
- Buat 2 model baru `models/master_dropdown.py`:
  ```python
  from sqlalchemy import Column, String
  from models.base import BaseModel
  class KategoriPL(BaseModel):
      __tablename__="kategori_pl"; nama = Column(String(150), nullable=False)
  class JenisMK(BaseModel):
      __tablename__="jenis_mk"; nama = Column(String(100), nullable=False)
  ```
- Daftarkan di `db/migrate.py` `_import_all_models()`.
- Seed (di `seed_all`): KategoriPL = ["PL Penciri Utama","PL Sikap","PL Keterampilan Umum dan Sikap","PL Tambahan KK dan P"]; JenisMK = ["MK Wajib","MK Pilihan","MKWK","MKDU"]. (Lihat `master_kategori_pl` & `master_jenis_mk` di `sistem_kurikulum_obe (2).sql` baris 229–240.)
- Endpoint CRUD ringkas `routes/master_dropdown.py` (GET/POST `/api/kategori-pl`, `/api/jenis-mk`) — daftarkan di `routes/registry.py`.
- Frontend: di form Profil Lulusan & Mata Kuliah, ganti input teks kategori/jenis jadi `<select>` yang di-load dari endpoint tsb. (lihat `static/js/pages/master_data.js`).

## T4. Kolom REFERENSI untuk CPL & Bahan Kajian (+ tooltip hover)
Klien minta CPL & BK punya kolom **referensi** yang tampil saat **hover**.
- Pastikan model `CPLProdi` punya field `referensi` / `referensi_standar` (cek `models/cpl.py`; SQL baseline pakai `referensi_standar`). Tambah field `referensi` pada `BahanKajian` (`models/bahan_kajian.py`) bila belum ada → daftarkan di `_NEW_COLUMNS` `db/migrate.py` (`("bahan_kajian","referensi","VARCHAR(255)")`, `("cpl_prodi","referensi_standar","VARCHAR(255)")`).
- Frontend: tampilkan ikon/teks dengan `title="..."` (tooltip) di kolom kode CPL/BK pada tabel & matriks.

## T5. Aksi VALIDASI / KUNCI (lock) di semua bagian
Klien: selain CRUD, ada aksi **validasi = mengunci** dokumen di semua bagian.
- `master_periode_kurikulum` sudah punya `locked`/`is_locked`. Tambah pola serupa: saat periode `locked=True`, **tolak** semua POST/PUT/DELETE master data periode itu.
- Implementasi paling aman & terpusat: di handler create/update/delete master (`routes/master_*.py`), sebelum menulis, cek periode aktif terkait → kalau `locked`, `return error("Periode terkunci", status=423)`. Buat helper `services/lock_guard.py: assert_periode_unlocked(periode_id)`.
- Frontend: tombol "Kunci/Buka Kunci" (action `lock_periode`) di halaman periode; saat terkunci, sembunyikan tombol Tambah/Edit/Hapus (disable).

## T6. Perbaiki visual matriks CPL-PL (kolom CPL kelebaran)
Klien: di matriks CPL-PL, kolom CPL terlalu lebar (seolah ada deskripsi padahal hanya kode). 
- Di `static/css/matrix.css`: beri lebar tetap kecil untuk kolom kode (mis. `.matrix-row-header{ max-width:90px; white-space:nowrap; text-overflow:ellipsis; overflow:hidden; }`). Deskripsi cukup via tooltip `title=`. Uji di halaman "Matriks CPL - PL".

## T7. Pemetaan CPL-BK-MK & Peta Pemenuhan CPL = OTOMATIS (jangan manual)
Klien tegas: jangan input manual; **turunkan otomatis** dari relasi yang sudah ada.
- **Pemetaan CPL-BK-MK** (`routes/pemetaan_cpl_bk_mk.py`): hasil = gabungan `relasi_cpl_bk` (mapping_cpl_bk) JOIN `relasi_bk_mk` (mapping_bk_mk). Tampilkan komposit: **MK di tengah, CPL di atas, BK di dalam**, detail saat hover. Referensi tampilan: Tabel 10 buku panduan & VIEW `view_matriks_cpl_bk_mk` di `sistem_kurikulum_obe (2).sql` baris 441–455 (tiru query JOIN-nya).
- **Peta Pemenuhan CPL (Tabel 11)** (`routes/peta_cpl.py`): turunkan dari `mapping_cpl_mk` JOIN `master_mata_kuliah.semester_penempatan`. Bentuk: baris = CPL, kolom = Semester 1..8, isi sel = daftar MK + jumlah SKS. **Hitung otomatis**, jangan ada input manual.
- Uji: ubah satu relasi CPL-BK → pemetaan CPL-BK-MK & peta pemenuhan ikut berubah tanpa input manual.

## T8. RPS sesuai TEMPLATE buku panduan + bisa dicetak
Klien: input RPS ikut template di sheet "Rancangan RPS" (buku panduan hal. 42–45). Struktur: identitas MK, dosen pengampu, CPMK, Sub-CPMK, pemetaan Sub-CPMK↔CPMK, lalu **per pertemuan (16 minggu)** berisi Sub-CPMK, indikator, kriteria, metode, materi, bobot%.
- Cocokkan model dengan `rps_utama`, `rps_dosen_pengampu`, `rps_cpmk`, `rps_sub_cpmk`, `rps_pertemuan_mingguan` di `sistem_kurikulum_obe (2).sql` baris 168–221 (tambah field yang kurang: `bobot_teori_sks`, `bobot_praktikum_sks`, `pustaka_utama/pendukung`, `media_software/hardware`, `mk_prasyarat`).
- **Cetak:** sediakan tombol "Cetak/PDF" yang membuka tampilan print (CSS `@media print`) menyerupai template; pakai `window.print()`. (Export PDF rapi = boleh tahap berikutnya.)

## T9. Halaman "REFERENSI" (peta 3 sumber per fitur)
Klien ingin tiap fitur menunjukkan sumber: **Buku Panduan (tabel/halaman)**, **Spreadsheet (sheet)**, **LEDIK/PIKOBE (tabel)**. Buat halaman statis read-only `static/js/pages/referensi_page.js` berisi tabel berikut (sumber: tabel yang dikirim pemilik). Daftarkan di sidebar (section paling bawah) & `router.js`:

| Sidebar | Rancangan Kurikulum | Buku Kurikulum | PIKOBE |
|---|---|---|---|
| identitas prodi | — | Tabel A Isian identitas (hal 6) | — |
| profil lulusan | — | Tabel 1 Profil Lulusan (hal 15) | — |
| CPL Prodi | Sheet 3. CPL Prodi | Tabel 2 CPL Kompetensi Utama (hal 17) | Tabel 2 Capaian Pembelajaran Lulusan |
| Bahan Kajian | Sheet 6. Bahan Kajian | Tabel 4 Rumusan Bahan Kajian (hal 19-20) | — |
| Mata Kuliah | Sheet 11. Susunan Mata Kuliah | Tabel 9 Susunan Mata Kuliah (hal 26-27) | — |
| CPMK | — | Tabel 12 Pemetaan CPL-CPMK-MK (hal 31) | — |
| matriks cpl-pl | — | Tabel 3 Pemetaan CPL dan PL (hal 18) | — |
| matriks cpl-bk | — | Tabel 5 Pemetaan CPL-BK (hal 21) | — |
| matriks bk-mk | — | Tabel 6 Pemetaan BK-MK (hal 22) | — |
| matriks cpl-mk | — | Tabel 7 Pemetaan CPL-MK (hal 24) | — |
| matriks cpmk-mk | — | Tabel 14 Pemetaan MK-CPL-CPMK (hal 33) | — |
| pemetaan cpl-bk-mk | — | Tabel 8 Pemetaan BK-CPL-MK (hal 24) | — |
| organisasi mk | — | Tabel 10 Organisasi Mata Kuliah (hal 29) | — |
| peta pemenuhan cpl | — | Tabel 11 Peta Pemenuhan CPL (hal 30) | — |
| mk-cpmk-sub cpmk | — | Tabel 15 Pemetaan MK-CPMK-Sub-CPMK (hal 35) | — |
| rps | Sheet 21. Rancangan RPS | 4. RPS (hal 42-45) | Sheet Contoh RPS |

---

# BAGIAN 3 — CELAH & JEBAKAN (WAJIB dihindari)
1. **Jangan simpan upload ke disk di produksi** → hilang di Vercel. Pakai `storage_service.save_pdf` (Supabase). Kalau lupa set env Supabase, upload jatuh ke disk lokal & TIDAK persist di Vercel.
2. **Setelah ubah model (tambah kolom), kolom tidak otomatis ada di Supabase.** Tambah ke `_NEW_COLUMNS` di `db/migrate.py`, lalu buka `/api/db-status?token=<DB_ADMIN_TOKEN>&init=1` di produksi. Lokal: hapus `kurikulum_obe.db` lalu jalankan ulang.
3. **`?init=1` melewati seeding bila data sudah ada** (anti-duplikat). Jadi di DB lama, akun/role baru TIDAK otomatis terbuat. Buat akun via menu Manajemen Pengguna atau kosongkan DB dulu.
4. **OPEN ACCESS ≠ tanpa login.** User tetap harus login (ada `login_required`). Yang dibuka hanya pembatasan per-role. Jangan hapus `login_required`.
5. **Jangan kirim `password_hash` ke frontend.** Selalu lewat `_build_session_payload` / `_user_public`.
6. **Periode 5 tahun = +4** (inklusif). Jangan +5.
7. **Konsistensi tipe DB:** jangan jalankan `sistem_kurikulum_obe (2).sql` (MySQL: `YEAR`, `AUTO_INCREMENT`, `BOOLEAN`) langsung ke Supabase/Postgres — error/typemismatch. Itu hanya referensi data & relasi.
8. **Commit tanpa trailer `Co-Authored-By`** & author = pemilik repo, kalau tidak Vercel Hobby memblokir deploy ("commit author did not have contributing access").
9. **Jangan ubah nama key halaman di `router.js`** saat reorganisasi sidebar (T2) — cukup pindah antar-section di `sidebar.js`. Mengubah key memutus navigasi.
10. **Jangan hapus struktur role/permission** saat menerapkan open access — hanya bypass lewat flag, supaya gampang diaktifkan lagi.
11. **Setiap selesai 1 langkah: jalankan `py_compile` + `pytest` + smoke test.** Kalau merah, perbaiki dulu sebelum lanjut. Jangan menumpuk perubahan tanpa verifikasi.
12. **Drag-and-drop upload pakai `FormData`+`fetch`**, BUKAN wrapper `Api` (yang mengirim JSON). Salah pakai → file tidak terkirim.

---

# BAGIAN 4 — URUTAN EKSEKUSI (checklist sequential)
Kerjakan dari atas ke bawah. Centang tiap selesai + commit.
1. [ ] Baca Bagian 0 (konteks + fakta teknis). Jalankan `py_compile` & `pytest` baseline (pastikan hijau sebelum mulai).
2. [ ] **R1** Periode 5 tahun → verifikasi → commit.
3. [ ] **R2** Modul dokumen/notulensi/reuni + PDF → verifikasi → commit.
4. [ ] **R3** Role + OPEN ACCESS → verifikasi (semua endpoint 200/201) → commit.  ← jangan lewat
5. [ ] **T1** Sidebar collapsible → commit.
6. [ ] **T2** Reorg PLAN/DO/CHECK → commit.
7. [ ] **T3** Master data Kategori PL & Jenis MK → commit.
8. [ ] **T4** Kolom referensi CPL & BK → commit.
9. [ ] **T5** Aksi lock/validasi → commit.
10. [ ] **T6** Fix visual matriks CPL-PL → commit.
11. [ ] **T7** Pemetaan CPL-BK-MK & peta pemenuhan CPL otomatis → commit.
12. [ ] **T8** RPS template + cetak → commit.
13. [ ] **T9** Halaman Referensi → commit.
14. [ ] **VERIFIKASI AKHIR**: `pytest` hijau; login tiap role → semua menu kebuka tanpa 403; periode 5 thn; agenda reuni + upload PDF jalan & persist; sidebar bisa ditutup; matriks di PLAN, DO cuma RPS.
15. [ ] Push ke `main` (Vercel auto-deploy). Set env Supabase + bucket. Jalankan `/api/db-status?token=...&init=1` bila perlu migrasi kolom.

**Akun demo (sesudah seed):** `admin`/`admin123`, `kaprodi`/`kaprodi`, `timkurikulum`/`timkurikulum`, `dosen`/`dosen`, `2024001`/`2024001` (mahasiswa). Karena OPEN ACCESS, semuanya bisa akses semua menu.

> Penutup: kalau ragu pada langkah mana pun → **STOP, baca file sumber yang disebut, jangan berasumsi.** Lebih baik tanya daripada salah arsitektur.
