"""
Schema creation dan migration.
Membuat semua tabel berdasarkan model definitions.
"""

import state
from models.base import Base


def create_all():
    """Membuat seluruh tabel yang terdefinisi di models."""
    _import_all_models()
    Base.metadata.create_all(bind=state.engine)


def drop_all():
    """Menghapus seluruh tabel. Hanya untuk development/testing."""
    _import_all_models()
    Base.metadata.drop_all(bind=state.engine)


def reset_db():
    """Drop lalu create ulang semua tabel."""
    drop_all()
    create_all()


def _import_all_models():
    """
    Import semua module model agar SQLAlchemy
    mengetahui seluruh tabel yang perlu dibuat.
    """
    import models.institution
    import models.period
    import models.user
    import models.profil_lulusan
    import models.cpl
    import models.bahan_kajian
    import models.mata_kuliah
    import models.cpmk
    import models.sub_cpmk
    import models.mapping
    import models.penilaian
    import models.nilai
    import models.rps
    import models.log_peninjauan
