"""
Import data awal dari referensi Rancangan Kurikulum SI.
Data diambil langsung dari file Excel yang sudah di-extract.
"""

import state
from models.period import PeriodeKurikulum
from models.profil_lulusan import ProfilLulusan
from models.cpl import CPLProdi, CPLSNDikti
from models.bahan_kajian import BahanKajian
from models.mata_kuliah import MataKuliah
from models.institution import Universitas, Fakultas, ProgramStudi


def seed_institution():
    """Membuat data institusi default."""
    session = state.db

    univ = Universitas(nama="Universitas Contoh", alamat="Jl. Contoh No. 1")
    session.add(univ)
    session.flush()

    fak = Fakultas(universitas_id=univ.id, nama="Fakultas Teknik")
    session.add(fak)
    session.flush()

    prodi = ProgramStudi(
        fakultas_id=fak.id,
        nama="Sistem Informasi",
        jenjang="S1",
        akreditasi="Unggul",
        visi="Menjadi program studi unggulan",
        gelar_lulusan="S.Kom",
    )
    session.add(prodi)
    session.flush()
    return prodi.id


def seed_periode(prodi_id):
    """
    Membuat periode kurikulum (5 tahunan).
    Periode aktif 2024-2028 + satu periode berikutnya 2029-2033 (draft)
    agar pemisahan dokumen antar-generasi & dropdown periode dapat diuji.
    Mengembalikan id periode aktif.
    """
    session = state.db
    periode = PeriodeKurikulum(
        prodi_id=prodi_id,
        nama="Kurikulum 2024-2028",
        tahun_mulai=2024,
        tahun_selesai=2028,
        status="aktif",
    )
    session.add(periode)
    session.flush()

    periode_berikutnya = PeriodeKurikulum(
        prodi_id=prodi_id,
        nama="Kurikulum 2029-2033",
        tahun_mulai=2029,
        tahun_selesai=2033,
        status="draft",
    )
    session.add(periode_berikutnya)
    session.flush()

    return periode.id


def seed_profil_lulusan(pid):
    """Seed PL dari Sheet 1. Profil Lulusan."""
    data = [
        ("PL1", "Lulusan memiliki kemampuan untuk merencanakan, menganalisis, merancang, membangun, mengujicoba, menerapkan, dan mengevaluasi sistem informasi dalam sebuah proyek yang selaras dengan tujuan organisasi", "Penciri Utama"),
        ("PL2", "Lulusan memiliki kemampuan memahami, menerapkan, dan mengintegrasikan model bisnis dengan menggunakan metode dan berbagai teknik peningkatan bisnis proses yang mendatangkan suatu nilai tambah bagi organisasi", "Penciri Utama"),
        ("PL3", "Lulusan memiliki kemampuan untuk mengolah, menganalisis, dan menyajikan data yang dikembangkan dengan konsep big data dan business intelligence untuk membantu dalam proses pengambilan keputusan", "Tambahan KK dan P"),
        ("PL4", "Lulusan memiliki sikap religius, beretika, dan peka terhadap lingkungan sosial sebagai seorang warga negara dengan berlandaskan nilai ahlussunah waljamaah (Aswaja)", "Sikap"),
        ("PL5", "Lulusan memiliki kemampuan berpikir kritis dan inovatif, bekerja mandiri, membuat keputusan tepat, mendokumentasikan data dengan benar, menyusun karya ilmiah, berkomunikasi efektif", "Keterampilan Umum dan Sikap"),
    ]
    for kode, desk, kat in data:
        state.db.add(ProfilLulusan(periode_id=pid, kode=kode, deskripsi=desk, kategori=kat))
    state.db.flush()
