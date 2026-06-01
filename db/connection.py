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
    is_sqlite = config.DATABASE_URI.startswith("sqlite")

    engine_args = {
        "echo": config.DATABASE_ECHO,
    }

    if not is_sqlite:
        engine_args["pool_pre_ping"] = True
        engine_args["pool_recycle"] = 300

    state.engine = create_engine(config.DATABASE_URI, **engine_args)

    session_factory = sessionmaker(bind=state.engine)
    state.db = scoped_session(session_factory)

    return state.engine, state.db


def close_db():
    """Menutup session dan dispose engine."""
    if state.db is not None:
        state.db.remove()

    if state.engine is not None:
        state.engine.dispose()
