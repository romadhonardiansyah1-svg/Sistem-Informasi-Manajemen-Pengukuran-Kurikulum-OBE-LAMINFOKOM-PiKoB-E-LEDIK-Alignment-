"""
Model CPL: CPL SN-Dikti dan CPL Prodi.
Mengacu pada Tabel 2 dan Tabel 4 Buku Panduan APTIKOM.

CPL SN-Dikti memiliki 4 kategori: S (Sikap), KU (Keterampilan Umum),
KK (Keterampilan Khusus), P (Pengetahuan).

CPL Prodi adalah turunan yang ditetapkan oleh program studi.
Contoh: CPL01 - CPL14.
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text

from models.base import BaseModel


class CPLSNDikti(BaseModel):
    __tablename__ = "cpl_sn_dikti"

    periode_id = Column(Integer, ForeignKey("periode_kurikulum.id"), nullable=False)
    kode = Column(String(20), nullable=False)
    kategori = Column(String(10), nullable=False)  # S, KU, KK, P
    deskripsi = Column(Text, nullable=False)
    referensi = Column(Text)


class CPLProdi(BaseModel):
    __tablename__ = "cpl_prodi"

    periode_id = Column(Integer, ForeignKey("periode_kurikulum.id"), nullable=False)
    kode = Column(String(10), nullable=False)
    deskripsi = Column(Text, nullable=False)
    referensi = Column(Text)
