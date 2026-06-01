"""
Model CPMK (Capaian Pembelajaran Mata Kuliah).
Mengacu pada Tabel 12 dan 13 Buku Panduan APTIKOM.

Setiap CPMK adalah turunan dari satu CPL Prodi.
Contoh: CPL01 -> CPMK011, CPMK012
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text

from models.base import BaseModel


class CPMK(BaseModel):
    __tablename__ = "cpmk"

    cpl_id = Column(Integer, ForeignKey("cpl_prodi.id"), nullable=False)
    kode = Column(String(20), nullable=False)
    deskripsi = Column(Text, nullable=False)
