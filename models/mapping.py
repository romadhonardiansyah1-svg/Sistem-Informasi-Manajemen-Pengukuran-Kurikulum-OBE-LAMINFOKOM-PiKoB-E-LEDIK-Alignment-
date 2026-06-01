"""
Tabel asosiasi many-to-many untuk seluruh pemetaan.
Setiap tabel asosiasi menyimpan pasangan foreign key.

Mapping:
  - CPL-PL         (Tabel 3)
  - CPL SN-Dikti   (Tabel 4)
  - CPL-BK         (Tabel 5)
  - BK-MK          (Tabel 6)
  - CPL-MK         (Tabel 7)
  - CPMK-MK        (Tabel 12/13/14)
"""

from sqlalchemy import Table, Column, Integer, ForeignKey

from models.base import Base


mapping_cpl_pl = Table(
    "mapping_cpl_pl",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("cpl_id", Integer, ForeignKey("cpl_prodi.id"), nullable=False),
    Column("pl_id", Integer, ForeignKey("profil_lulusan.id"), nullable=False),
)


mapping_cpl_sndikti = Table(
    "mapping_cpl_sndikti",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("cpl_prodi_id", Integer, ForeignKey("cpl_prodi.id"), nullable=False),
    Column("cpl_sn_id", Integer, ForeignKey("cpl_sn_dikti.id"), nullable=False),
)


mapping_cpl_bk = Table(
    "mapping_cpl_bk",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("cpl_id", Integer, ForeignKey("cpl_prodi.id"), nullable=False),
    Column("bk_id", Integer, ForeignKey("bahan_kajian.id"), nullable=False),
)


mapping_bk_mk = Table(
    "mapping_bk_mk",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("bk_id", Integer, ForeignKey("bahan_kajian.id"), nullable=False),
    Column("mk_id", Integer, ForeignKey("mata_kuliah.id"), nullable=False),
)


mapping_cpl_mk = Table(
    "mapping_cpl_mk",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("cpl_id", Integer, ForeignKey("cpl_prodi.id"), nullable=False),
    Column("mk_id", Integer, ForeignKey("mata_kuliah.id"), nullable=False),
)


mapping_cpmk_mk = Table(
    "mapping_cpmk_mk",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("cpmk_id", Integer, ForeignKey("cpmk.id"), nullable=False),
    Column("mk_id", Integer, ForeignKey("mata_kuliah.id"), nullable=False),
)
