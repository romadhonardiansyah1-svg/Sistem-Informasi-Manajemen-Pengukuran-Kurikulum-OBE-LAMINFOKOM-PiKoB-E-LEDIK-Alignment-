"""
Seed data demo penilaian (TahapPenilaian + BobotPenilaian) dan
nilai mahasiswa (NilaiMahasiswa).

Tujuan: memberi data acuan yang LENGKAP dan PROFESIONAL agar pipeline
kalkulasi berjenjang (Nilai -> CPMK -> MK -> CPL) menghasilkan angka nyata
dan bervariasi, sehingga laporan CPL, spider chart, dan halaman cetak
penilaian tidak pernah kosong.

Aturan bobot:
- TahapPenilaian.bobot: bobot CPMK DI DALAM sebuah MK. Total seluruh tahap
  (CPMK) per MK = 100, sehingga nilai MK = rata-rata tertimbang yang valid
  (0-100). Ini yang dipakai engine kalkulasi.
- BobotPenilaian: distribusi bobot PER TEKNIK penilaian untuk tiap CPMK
  (Tabel 18/18a). Total per baris (per CPMK) = 100. Dipakai untuk menghitung
  skor_total tiap NilaiMahasiswa secara konsisten dari komponen-komponennya.
"""

import config
import state
from models.cpmk import CPMK
from models.penilaian import TahapPenilaian, BobotPenilaian
from models.nilai import NilaiMahasiswa
from models.user import Mahasiswa
from models.mapping import mapping_cpmk_mk


# Profil distribusi bobot per teknik penilaian (partisipasi, observasi,
# unjuk_kerja, uts, uas, tes_lisan). Setiap profil berjumlah 100.
# Dipilih bergiliran per CPMK agar realistis & bervariasi antar MK/CPMK.
_PROFIL_BOBOT = [
    # (partisipasi, observasi, unjuk_kerja, uts, uas, tes_lisan)
    (10, 10, 20, 30, 30, 0),   # teori seimbang
    (10, 15, 35, 20, 20, 0),   # praktik / proyek dominan
    (15, 10, 25, 15, 20, 15),  # dilengkapi tes lisan
    (5, 5, 15, 35, 40, 0),     # ujian tulis dominan
]

# Label ringkas teknik untuk membangun teks teknik penilaian.
_TEKNIK_LABEL = [
    ("partisipasi", "Partisipasi"),
    ("observasi", "Observasi"),
    ("unjuk_kerja", "Unjuk Kerja"),
    ("uts", "UTS"),
    ("uas", "UAS"),
    ("tes_lisan", "Tes Lisan"),
]

_TAHAP_CYCLE = ("awal_tengah", "tengah_akhir", "awal_akhir")
_INSTRUMEN_CYCLE = config.INSTRUMEN_CHOICES
_KRITERIA_CYCLE = (
    "Ketepatan konsep, kelengkapan analisis, dan kedalaman argumentasi.",
    "Kebenaran solusi, kerapian implementasi, dan ketepatan waktu.",
    "Kemampuan komunikasi, kerja sama tim, dan kualitas presentasi.",
    "Ketelitian, sistematika penyelesaian, dan orisinalitas karya.",
)


def _profil_for(cpmk_id):
    """Pilih profil bobot teknik secara deterministik berdasarkan CPMK."""
    return _PROFIL_BOBOT[cpmk_id % len(_PROFIL_BOBOT)]


def _teknik_text(profil):
    """Bangun teks teknik penilaian dari profil bobot (hanya yang > 0)."""
    parts = []
    for (key, label), pct in zip(_TEKNIK_LABEL, profil):
        if pct > 0:
            parts.append("{} {}%".format(label, pct))
    return ", ".join(parts)


def seed_tahap_penilaian():
    """
    Buat TahapPenilaian + BobotPenilaian untuk tiap pasangan (CPMK, MK)
    yang dipetakan. Idempotent: dilewati bila data sudah ada.
    """
    session = state.db
    if session.query(TahapPenilaian).count() > 0:
        return

    cpl_of_cpmk = {c.id: c.cpl_id for c in session.query(CPMK).all()}

    # Kumpulkan pasangan (mk_id -> [(cpmk_id, cpl_id), ...]) dari mapping CPMK-MK.
    per_mk = {}
    for row in session.execute(mapping_cpmk_mk.select()).fetchall():
        cpl_id = cpl_of_cpmk.get(row.cpmk_id)
        if cpl_id is None:
            continue
        per_mk.setdefault(row.mk_id, []).append((row.cpmk_id, cpl_id))

    has_bobot = session.query(BobotPenilaian).count() > 0

    for mk_id, pairs in per_mk.items():
        n = len(pairs)
        base = 100 // n
        sisa = 100 - base * n  # dibebankan ke tahap pertama agar total tepat 100
        for idx, (cpmk_id, cpl_id) in enumerate(pairs):
            bobot = base + (sisa if idx == 0 else 0)
            profil = _profil_for(cpmk_id)

            session.add(TahapPenilaian(
                cpl_id=cpl_id,
                mk_id=mk_id,
                cpmk_id=cpmk_id,
                tahap=_TAHAP_CYCLE[idx % len(_TAHAP_CYCLE)],
                teknik_penilaian_text=_teknik_text(profil),
                instrumen=_INSTRUMEN_CYCLE[idx % len(_INSTRUMEN_CYCLE)],
                kriteria=_KRITERIA_CYCLE[idx % len(_KRITERIA_CYCLE)],
                bobot=bobot,
            ))

            if not has_bobot:
                p_part, p_obs, p_unjuk, p_uts, p_uas, p_lisan = profil
                session.add(BobotPenilaian(
                    cpl_id=cpl_id,
                    mk_id=mk_id,
                    cpmk_id=cpmk_id,
                    partisipasi_pct=p_part,
                    observasi_pct=p_obs,
                    unjuk_kerja_pct=p_unjuk,
                    uts_pct=p_uts,
                    uas_pct=p_uas,
                    tes_lisan_pct=p_lisan,
                    total=p_part + p_obs + p_unjuk + p_uts + p_uas + p_lisan,
                ))

    session.flush()


def _komponen_skor(base, cpmk_id, tech_idx):
    """
    Skor satu komponen teknik untuk satu mahasiswa, bervariasi & deterministik.
    Rentang dijaga 45-100 agar realistis (tidak ada 0).
    """
    delta = ((cpmk_id * 7 + tech_idx * 13 + 5) % 23) - 11  # -11..+11
    return float(max(45, min(100, base + delta)))


def seed_nilai_demo():
    """
    Buat nilai untuk tiap mahasiswa demo pada setiap tahap penilaian.

    Skor tiap komponen teknik bervariasi per mahasiswa & per CPMK secara
    deterministik. skor_total dihitung sebagai rata-rata tertimbang komponen
    menggunakan persentase pada BobotPenilaian (Tabel 18/18a) sehingga
    konsisten end-to-end. Hasilnya: sebagian CPL di atas dan sebagian di bawah
    KKM (variasi realistis untuk laporan & spider chart).
    """
    session = state.db
    if session.query(NilaiMahasiswa).count() > 0:
        return

    mhs_list = session.query(Mahasiswa).order_by(Mahasiswa.id).all()
    tahap_list = session.query(TahapPenilaian).all()
    if not mhs_list or not tahap_list:
        return

    # Lookup distribusi bobot teknik per (mk_id, cpmk_id).
    bobot_map = {}
    for bp in session.query(BobotPenilaian).all():
        bobot_map[(bp.mk_id, bp.cpmk_id)] = bp

    for si, mhs in enumerate(mhs_list):
        base = 90 - si * 5  # 90, 85, 80, 75, 70 (variasi antar mahasiswa)
        for tahap in tahap_list:
            cid = tahap.cpmk_id
            skor_partisipasi = _komponen_skor(base, cid, 0)
            skor_observasi = _komponen_skor(base, cid, 1)
            skor_unjuk_kerja = _komponen_skor(base, cid, 2)
            skor_uts = _komponen_skor(base, cid, 3)
            skor_uas = _komponen_skor(base, cid, 4)
            skor_tes_lisan = _komponen_skor(base, cid, 5)

            bp = bobot_map.get((tahap.mk_id, cid))
            if bp is not None and (bp.total or 0) > 0:
                total = (
                    skor_partisipasi * (bp.partisipasi_pct or 0)
                    + skor_observasi * (bp.observasi_pct or 0)
                    + skor_unjuk_kerja * (bp.unjuk_kerja_pct or 0)
                    + skor_uts * (bp.uts_pct or 0)
                    + skor_uas * (bp.uas_pct or 0)
                    + skor_tes_lisan * (bp.tes_lisan_pct or 0)
                ) / float(bp.total)
            else:
                # Fallback: rata-rata sederhana komponen ujian + tugas.
                total = (
                    skor_unjuk_kerja + skor_uts + skor_uas
                ) / 3.0

            session.add(NilaiMahasiswa(
                mahasiswa_id=mhs.id,
                mk_id=tahap.mk_id,
                cpmk_id=cid,
                semester_aktif="2024/2025-Ganjil",
                skor_partisipasi=skor_partisipasi,
                skor_observasi=skor_observasi,
                skor_unjuk_kerja=skor_unjuk_kerja,
                skor_uts=skor_uts,
                skor_uas=skor_uas,
                skor_tes_lisan=skor_tes_lisan,
                skor_total=round(total, 2),
            ))

    session.flush()
