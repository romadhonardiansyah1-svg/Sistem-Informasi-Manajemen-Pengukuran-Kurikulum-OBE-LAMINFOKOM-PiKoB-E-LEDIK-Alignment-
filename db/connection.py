"""
Inisialisasi koneksi database menggunakan SQLAlchemy.
Dipanggil sekali saat startup aplikasi.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import config
import state


def init_db():
    """
    Membuat engine dan session factory.
    Menyimpan referensi ke state.engine dan state.db.
    """
    state.engine = create_engine(
        config.DATABASE_URI,
        echo=config.DATABASE_ECHO,
        pool_pre_ping=True,
    )

    session_factory = sessionmaker(bind=state.engine)
    state.db = scoped_session(session_factory)

    return state.engine, state.db


def close_db():
    """Menutup session dan dispose engine."""
    if state.db is not None:
        state.db.remove()

    if state.engine is not None:
        state.engine.dispose()
