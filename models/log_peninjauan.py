"""
Model Agenda Penjaminan Mutu (sebelumnya "log peninjauan") dan dokumen bukti fisik.

Satu modul untuk seluruh kegiatan penjaminan mutu:
- Peninjauan Kurikulum
- Reuni Alumni
- FGD / Lokakarya
- Rapat Mutu

Setiap agenda menyimpan notulensi (kolom `catatan`) dan dapat memiliki banyak
dokumen PDF (notulen, presensi, undangan, dsb) via DokumenBukti.
T-13.1 / T-13.2 Backlog.
"""

from sqlalchemy import Column, String, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from models.base import BaseModel


class LogPeninjauan(BaseModel):
    __tablename__ = "log_peninjauan"

    jenis = Column(String(40), nullable=False, default="peninjauan_kurikulum")
    periode_id = Column(Integer, ForeignKey("periode_kurikulum.id"), nullable=True)
    judul = Column(String(300), nullable=False)
    tanggal = Column(Date, nullable=False)
    lokasi = Column(String(200))
    peserta = Column(Text)
    catatan = Column(Text)   # notulensi
    status = Column(String(50), default="draft")

    dokumen_list = relationship(
        "DokumenBukti",
        back_populates="log_peninjauan",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )


class DokumenBukti(BaseModel):
    __tablename__ = "dokumen_bukti"

    log_id = Column(Integer, ForeignKey("log_peninjauan.id"), nullable=False)
    filename = Column(String(300), nullable=False)
    filepath = Column(String(500), default="")          # path lokal (backend=local)
    storage_key = Column(String(500), default="")        # key di Supabase Storage
    storage_backend = Column(String(20), default="local")  # local | supabase
    tipe = Column(String(50), default="bukti_fisik")
    ukuran = Column(Integer, default=0)

    log_peninjauan = relationship("LogPeninjauan", back_populates="dokumen_list")
