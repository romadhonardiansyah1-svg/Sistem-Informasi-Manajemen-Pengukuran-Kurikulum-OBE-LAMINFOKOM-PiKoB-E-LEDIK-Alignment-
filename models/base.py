"""
Base model class dan mixin.
Semua model mewarisi dari Base dan menggunakan TimestampMixin.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TimestampMixin:
    """Mixin untuk kolom created_at dan updated_at."""

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class BaseModel(Base, TimestampMixin):
    """
    Base model dengan id auto-increment dan timestamp.
    Semua model mewarisi dari class ini.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    def to_dict(self):
        """Konversi instance ke dictionary."""
        result = {}
        for col in self.__table__.columns:
            value = getattr(self, col.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[col.name] = value
        return result
