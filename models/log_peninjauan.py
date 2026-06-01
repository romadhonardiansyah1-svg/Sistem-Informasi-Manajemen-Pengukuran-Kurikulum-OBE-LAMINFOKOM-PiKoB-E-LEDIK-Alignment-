"""
Model log peninjauan kurikulum dan dokumen bukti fisik.
T-13.1 Backlog Notion.
"""

from sqlalchemy import Column, String, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from models.base import BaseModel


class LogPeninjauan(BaseModel):
    __tablename__ = "log_peninjauan"

    judul = Column(String(300), nullable=False)
    tanggal = Column(Date, nullable=False)
    peserta = Column(Text)
    catatan = Column(Text)
    status = Column(String(50), default="draft")

    dokumen_list = relationship(
        "DokumenBukti",
        back_populates="log_peninjauan",
        lazy="dynamic",
    )


class DokumenBukti(BaseModel):
    __tablename__ = "dokumen_bukti"

    log_id = Column(Integer, ForeignKey("log_peninjauan.id"), nullable=False)
    filename = Column(String(300), nullable=False)
    filepath = Column(String(500), nullable=False)
    tipe = Column(String(50), default="bukti_fisik")
    ukuran = Column(Integer, default=0)

    log_peninjauan = relationship("LogPeninjauan", back_populates="dokumen_list")
