"""
Model Profil Lulusan (PL).
Mengacu pada Tabel 1 Buku Panduan APTIKOM.
Contoh: PL01 - PL05.
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from models.base import BaseModel


class ProfilLulusan(BaseModel):
    __tablename__ = "profil_lulusan"

    periode_id = Column(Integer, ForeignKey("periode_kurikulum.id"), nullable=False)
    kode = Column(String(10), nullable=False)
    deskripsi = Column(Text, nullable=False)
    kategori = Column(String(50))  # utama, tambahan
    referensi = Column(Text)  # legacy, dipertahankan; nilai dimigrasikan ke ref_buku
    ref_buku = Column(Text)  # rujukan buku panduan (tabel/halaman)
    ref_spreadsheet = Column(Text)  # rujukan sheet rancangan kurikulum
    ref_pikobe = Column(Text)  # rujukan ledik/tabel PIKOBE
