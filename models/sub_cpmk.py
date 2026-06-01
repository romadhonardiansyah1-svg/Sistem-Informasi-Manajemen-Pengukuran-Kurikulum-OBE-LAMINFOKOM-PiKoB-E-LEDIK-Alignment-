"""
Model Sub-CPMK (Sub Capaian Pembelajaran Mata Kuliah).
Mengacu pada Tabel 15 Buku Panduan APTIKOM.

Setiap Sub-CPMK terikat pada satu CPMK dan satu MK.
Contoh: CPMK011 -> SubCPMK0111, SubCPMK0112
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text

from models.base import BaseModel


class SubCPMK(BaseModel):
    __tablename__ = "sub_cpmk"

    cpmk_id = Column(Integer, ForeignKey("cpmk.id"), nullable=False)
    mk_id = Column(Integer, ForeignKey("mata_kuliah.id"), nullable=False)
    kode = Column(String(30), nullable=False)
    deskripsi = Column(Text, nullable=False)
