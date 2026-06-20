"""
Model RPS (Rencana Pembelajaran Semester).
Mengacu pada template RPS di Buku Panduan APTIKOM halaman 42-45.

RPS terdiri dari header (per MK) dan detail mingguan (16 minggu).
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text, Float

from models.base import BaseModel


class RPS(BaseModel):
    __tablename__ = "rps"

    mk_id = Column(Integer, ForeignKey("mata_kuliah.id"), nullable=False)
    periode_id = Column(Integer, ForeignKey("periode_kurikulum.id"), nullable=False)
    kode_dokumen = Column(String(50))
    deskripsi_singkat = Column(Text)
    pustaka_utama = Column(Text)
    pustaka_pendukung = Column(Text)
    dosen_pengampu = Column(Text)
    dosen_koordinator = Column(String(200))
    tanggal_penyusunan = Column(String(20))
    bobot_teori_sks = Column(Integer, default=0)
    bobot_praktikum_sks = Column(Integer, default=0)
    media_software = Column(Text)
    media_hardware = Column(Text)
    mk_prasyarat = Column(Text)


class RPSMinggu(BaseModel):
    """
    Detail RPS per minggu.
    Minggu ke-8 = UTS, Minggu ke-16 = UAS.
    """
    __tablename__ = "rps_minggu"

    rps_id = Column(Integer, ForeignKey("rps.id"), nullable=False)
    minggu_ke = Column(Integer, nullable=False)
    sub_cpmk_id = Column(Integer, ForeignKey("sub_cpmk.id"), nullable=True)
    bentuk_pembelajaran = Column(Text)
    metode_luring = Column(Text)
    metode_daring = Column(Text)
    materi = Column(Text)
    bobot_penilaian_persen = Column(Float, default=0)
    indikator = Column(Text)
    kriteria_teknik = Column(Text)
