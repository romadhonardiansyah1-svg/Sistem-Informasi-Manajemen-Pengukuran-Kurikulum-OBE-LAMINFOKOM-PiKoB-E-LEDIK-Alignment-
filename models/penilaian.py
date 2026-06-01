"""
Model penilaian: TeknikPenilaian, TahapPenilaian, BobotPenilaian.
Mengacu pada Tabel 16, 17, 18, 18a Buku Panduan APTIKOM.

TeknikPenilaian  -- Boolean per teknik (Tabel 16)
TahapPenilaian   -- Tahap, instrumen, kriteria, bobot (Tabel 17)
BobotPenilaian   -- Persentase per teknik penilaian (Tabel 18/18a)
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text

from models.base import BaseModel


class TeknikPenilaian(BaseModel):
    """
    Tabel 16: pemetaan teknik penilaian per CPMK per MK.
    Setiap kolom boolean menunjukkan apakah teknik tersebut digunakan.
    """
    __tablename__ = "teknik_penilaian"

    cpl_id = Column(Integer, ForeignKey("cpl_prodi.id"), nullable=False)
    mk_id = Column(Integer, ForeignKey("mata_kuliah.id"), nullable=False)
    cpmk_id = Column(Integer, ForeignKey("cpmk.id"), nullable=False)
    partisipasi = Column(Boolean, default=False)
    observasi = Column(Boolean, default=False)
    unjuk_kerja = Column(Boolean, default=False)
    tes_tulis_uts = Column(Boolean, default=False)
    tes_tulis_uas = Column(Boolean, default=False)
    tes_lisan = Column(Boolean, default=False)


class TahapPenilaian(BaseModel):
    """
    Tabel 17: tahap, mekanisme, instrumen, kriteria, dan bobot penilaian.
    Bobot akumulasi per MK = 100.
    """
    __tablename__ = "tahap_penilaian"

    cpl_id = Column(Integer, ForeignKey("cpl_prodi.id"), nullable=False)
    mk_id = Column(Integer, ForeignKey("mata_kuliah.id"), nullable=False)
    cpmk_id = Column(Integer, ForeignKey("cpmk.id"), nullable=False)
    tahap = Column(String(30))  # awal_tengah, tengah_akhir, awal_akhir
    teknik_penilaian_text = Column(Text)
    instrumen = Column(Text)  # rubrik_holistik, rubrik_analitik, dll
    kriteria = Column(Text)
    bobot = Column(Integer, nullable=False, default=0)


class BobotPenilaian(BaseModel):
    """
    Tabel 18/18a: distribusi bobot per teknik penilaian per CPMK.
    Total per MK = 100.
    """
    __tablename__ = "bobot_penilaian"

    cpl_id = Column(Integer, ForeignKey("cpl_prodi.id"), nullable=False)
    mk_id = Column(Integer, ForeignKey("mata_kuliah.id"), nullable=False)
    cpmk_id = Column(Integer, ForeignKey("cpmk.id"), nullable=False)
    partisipasi_pct = Column(Integer, default=0)
    observasi_pct = Column(Integer, default=0)
    unjuk_kerja_pct = Column(Integer, default=0)
    uts_pct = Column(Integer, default=0)
    uas_pct = Column(Integer, default=0)
    tes_lisan_pct = Column(Integer, default=0)
    total = Column(Integer, default=0)
