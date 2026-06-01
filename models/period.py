"""
Model periode kurikulum 5 tahunan.
Setiap dokumen kurikulum terikat pada satu periode.
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models.base import BaseModel


class PeriodeKurikulum(BaseModel):
    __tablename__ = "periode_kurikulum"

    prodi_id = Column(Integer, ForeignKey("program_studi.id"), nullable=False)
    nama = Column(String(100), nullable=False)
    tahun_mulai = Column(Integer, nullable=False)
    tahun_selesai = Column(Integer, nullable=False)
    status = Column(String(20), default="draft")  # draft, aktif, arsip
    locked = Column(Boolean, default=False)

    prodi = relationship("ProgramStudi", back_populates="periode_list")
