"""
Model institusi: Universitas, Fakultas, ProgramStudi.
Struktur multi-level sesuai Stakeholder Vision Document.
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Universitas(BaseModel):
    __tablename__ = "universitas"

    nama = Column(String(200), nullable=False)
    alamat = Column(Text)

    fakultas_list = relationship("Fakultas", back_populates="universitas", lazy="dynamic")


class Fakultas(BaseModel):
    __tablename__ = "fakultas"

    universitas_id = Column(Integer, ForeignKey("universitas.id"), nullable=False)
    nama = Column(String(200), nullable=False)

    universitas = relationship("Universitas", back_populates="fakultas_list")
    prodi_list = relationship("ProgramStudi", back_populates="fakultas", lazy="dynamic")


class ProgramStudi(BaseModel):
    __tablename__ = "program_studi"

    fakultas_id = Column(Integer, ForeignKey("fakultas.id"), nullable=False)
    nama = Column(String(200), nullable=False)
    jenjang = Column(String(20), default="S1")
    akreditasi = Column(String(50))
    visi = Column(Text)
    misi = Column(Text)
    website = Column(String(200))
    email = Column(String(200))
    gelar_lulusan = Column(String(50))

    fakultas = relationship("Fakultas", back_populates="prodi_list")
    periode_list = relationship("PeriodeKurikulum", back_populates="prodi", lazy="dynamic")
