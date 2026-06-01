"""
Model nilai mahasiswa.
Menyimpan skor per komponen penilaian untuk setiap
kombinasi mahasiswa-MK-CPMK.
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Float

from models.base import BaseModel


class NilaiMahasiswa(BaseModel):
    __tablename__ = "nilai_mahasiswa"

    mahasiswa_id = Column(Integer, ForeignKey("mahasiswa.id"), nullable=False)
    mk_id = Column(Integer, ForeignKey("mata_kuliah.id"), nullable=False)
    cpmk_id = Column(Integer, ForeignKey("cpmk.id"), nullable=False)
    semester_aktif = Column(String(20))

    skor_partisipasi = Column(Float, default=0)
    skor_observasi = Column(Float, default=0)
    skor_unjuk_kerja = Column(Float, default=0)
    skor_uts = Column(Float, default=0)
    skor_uas = Column(Float, default=0)
    skor_tes_lisan = Column(Float, default=0)

    skor_total = Column(Float, default=0)
