"""
Model user dan mahasiswa.
Role didefinisikan di config.ROLES.
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nama = Column(String(200), nullable=False)
    email = Column(String(200))
    role = Column(String(50), nullable=False)
    prodi_id = Column(Integer, ForeignKey("program_studi.id"), nullable=True)
    fakultas_id = Column(Integer, ForeignKey("fakultas.id"), nullable=True)


class Mahasiswa(BaseModel):
    __tablename__ = "mahasiswa"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    nim = Column(String(20), unique=True, nullable=False)
    nama = Column(String(200), nullable=False)
    angkatan = Column(Integer, nullable=False)
    prodi_id = Column(Integer, ForeignKey("program_studi.id"), nullable=False)
