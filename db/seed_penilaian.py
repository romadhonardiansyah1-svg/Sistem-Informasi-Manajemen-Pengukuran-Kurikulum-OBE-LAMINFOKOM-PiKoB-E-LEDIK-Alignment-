"""
Seed data demo penilaian (TahapPenilaian) + nilai mahasiswa (NilaiMahasiswa).

Tujuan: memberi data acuan agar pipeline kalkulasi berjenjang
(Nilai -> CPMK -> MK -> CPL) menghasilkan angka nyata, sehingga laporan
CPL & spider chart mahasiswa tidak selalu 0.

Aturan bobot:
- Untuk setiap MK, total bobot seluruh tahap (CPMK di MK tsb) = 100,
  sehingga nilai MK = rata-rata tertimbang yang valid (0-100).
- Karena normalisasi CPL membagi dengan total bobot, skor CPL ter-normalisasi
  ~ rata-rata tertimbang skor_total CPMK terkait.
"""

import state
from models.cpmk import CPMK
from models.penilaian import TahapPenilaian
from models.nilai import NilaiMahasiswa
from models.user import Mahasiswa
from models.mapping import mapping_cpmk_mk


def seed_tahap_penilaian():
    """Buat satu tahap penilaian untuk tiap pasangan (CPMK, MK) yang dipetakan."""
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

    for mk_id, pairs in per_mk.items():
        n = len(pairs)
        base = 100 // n
        sisa = 100 - base * n  # dibebankan ke tahap pertama agar total tepat 100
        for idx, (cpmk_id, cpl_id) in enumerate(pairs):
            bobot = base + (sisa if idx == 0 else 0)
            session.add(TahapPenilaian(
                cpl_id=cpl_id,
                mk_id=mk_id,
                cpmk_id=cpmk_id,
                tahap="awal_akhir",
                teknik_penilaian_text="UTS, UAS, Tugas/Praktik",
                instrumen="rubrik_analitik",
                kriteria="Ketepatan, kelengkapan, dan kedalaman",
                bobot=bobot,
            ))

    session.flush()


def seed_nilai_demo():
    """
    Buat nilai untuk tiap mahasiswa demo pada setiap tahap penilaian.
    Skor bervariasi per mahasiswa & per CPMK secara deterministik
    sehingga sebagian CPL di atas dan sebagian di bawah KKM (variasi realistis).
    """
    session = state.db
    if session.query(NilaiMahasiswa).count() > 0:
        return

    mhs_list = session.query(Mahasiswa).order_by(Mahasiswa.id).all()
    tahap_list = session.query(TahapPenilaian).all()
    if not mhs_list or not tahap_list:
        return

    for si, mhs in enumerate(mhs_list):
        base = 88 - si * 5  # 88, 83, 78, 73, 68
        for ti, tahap in enumerate(tahap_list):
            # Variasi -10..+10 deterministik berdasarkan cpmk & urutan.
            delta = ((tahap.cpmk_id * 7 + ti * 3) % 21) - 10
            skor = max(40, min(100, base + delta))
            session.add(NilaiMahasiswa(
                mahasiswa_id=mhs.id,
                mk_id=tahap.mk_id,
                cpmk_id=tahap.cpmk_id,
                semester_aktif="2024/2025-Ganjil",
                skor_partisipasi=skor,
                skor_observasi=skor,
                skor_unjuk_kerja=skor,
                skor_uts=skor,
                skor_uas=skor,
                skor_tes_lisan=skor,
                skor_total=skor,
            ))

    session.flush()
