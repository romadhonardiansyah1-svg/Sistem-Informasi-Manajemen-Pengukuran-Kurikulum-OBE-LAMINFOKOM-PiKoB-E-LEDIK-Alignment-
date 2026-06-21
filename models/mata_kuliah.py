"""
Model Mata Kuliah (MK).
Mengacu pada Tabel 9 Buku Panduan APTIKOM.
Contoh: MK01 (Agama) - MK66 (Manajemen Rantai Pasok).
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean

from models.base import BaseModel


class MataKuliah(BaseModel):
    __tablename__ = "mata_kuliah"

    periode_id = Column(Integer, ForeignKey("periode_kurikulum.id"), nullable=False)
    kode = Column(String(10), nullable=False)
    nama = Column(String(200), nullable=False)
    sks = Column(Integer, nullable=False, default=3)
    semester = Column(Integer, nullable=False)
    jenis = Column(String(20), default="wajib")  # wajib, pilihan, mkwk, mkdu
    is_capstone = Column(Boolean, default=False)
    prasyarat = Column(Text)  # kode MK prasyarat, dipisah koma
    deskripsi_singkat = Column(Text)
    referensi = Column(Text)  # legacy/umum; nilai dimigrasikan ke ref_buku
    ref_buku = Column(Text)  # rujukan buku panduan (tabel/halaman)
    ref_spreadsheet = Column(Text)  # rujukan sheet rancangan kurikulum
    ref_pikobe = Column(Text)  # rujukan ledik/tabel PIKOBE
