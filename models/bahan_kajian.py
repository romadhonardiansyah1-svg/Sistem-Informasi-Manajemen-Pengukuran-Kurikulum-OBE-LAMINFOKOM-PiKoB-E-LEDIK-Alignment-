"""
Model Bahan Kajian (BK).
Mengacu pada Tabel 4 Buku Panduan APTIKOM.
Contoh: BK01 (Foundation of IS) - BK21 (Pemrograman Mobile).
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text

from models.base import BaseModel


class BahanKajian(BaseModel):
    __tablename__ = "bahan_kajian"

    periode_id = Column(Integer, ForeignKey("periode_kurikulum.id"), nullable=False)
    kode = Column(String(10), nullable=False)
    nama = Column(String(200), nullable=False)
    deskripsi = Column(Text)
    kompetensi = Column(String(20))  # utama, pendukung
    referensi = Column(Text)  # legacy, dipertahankan; nilai dimigrasikan ke ref_buku
    ref_buku = Column(Text)  # rujukan buku panduan (tabel/halaman)
    ref_spreadsheet = Column(Text)  # rujukan sheet rancangan kurikulum
    ref_pikobe = Column(Text)  # rujukan ledik/tabel PIKOBE
