"""
Inisialisasi koneksi database menggunakan SQLAlchemy.
Dipanggil sekali saat startup aplikasi.
"""

import os
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
    is_vercel = os.environ.get("VERCEL", "") == "1"

    engine_args = {
        "echo": config.DATABASE_ECHO,
    }

    if not is_sqlite:
        engine_args["pool_pre_ping"] = True

        if is_vercel:
            # Vercel serverless: NullPool - setiap request buat koneksi baru,
            # tidak ada koneksi stale yang bisa SSL drop.
            from sqlalchemy.pool import NullPool
            engine_args["poolclass"] = NullPool
        else:
            # Lokal: gunakan standard pool
            engine_args["pool_recycle"] = 280
            engine_args["pool_size"] = 2
            engine_args["max_overflow"] = 3

        engine_args["connect_args"] = {
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
            "connect_timeout": 10,
        }

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
