"""Shared FastAPI dependencies."""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Provide a database session and close it after the request."""
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()
