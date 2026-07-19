"""Base class for SQLAlchemy models."""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class shared by future persistence models."""

    metadata = MetaData(
        naming_convention={
            "ix": "idx_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


# Import persistence models so Alembic can discover their mapped tables.
from app.models.user import User  # noqa: E402, F401
