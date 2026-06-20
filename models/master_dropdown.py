"""
Model data master dropdown: Kategori PL dan Jenis MK.
Menjamin konsistensi data (misal "MKDU" vs "Mata Kuliah Bersama Universitas"
tidak dianggap beda) dengan menjadi pilihan dropdown, bukan input bebas.
"""

from sqlalchemy import Column, String

from models.base import BaseModel


class KategoriPL(BaseModel):
    __tablename__ = "kategori_pl"

    nama = Column(String(150), nullable=False)


class JenisMK(BaseModel):
    __tablename__ = "jenis_mk"

    nama = Column(String(100), nullable=False)
