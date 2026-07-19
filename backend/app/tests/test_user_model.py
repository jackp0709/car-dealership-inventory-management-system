"""Unit tests for the user model and repository."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository


def create_test_session() -> Session:
    """Return an isolated in-memory database session."""
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def test_user_model_assigns_defaults_and_timestamps() -> None:
    session = create_test_session()
    user = User(
        full_name="Ada Lovelace",
        email="ada@example.com",
        hashed_password="hashed-value",
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.role is UserRole.EMPLOYEE
    assert user.is_active is True
    assert user.created_at is not None
    assert user.updated_at is not None
    session.close()


def test_user_repository_performs_database_operations() -> None:
    session = create_test_session()
    repository = UserRepository(session)
    user = repository.create(
        User(
            full_name="Grace Hopper",
            email="grace@example.com",
            hashed_password="hashed-value",
            role=UserRole.ADMIN,
        )
    )

    assert repository.get_by_id(user.id) is user
    assert repository.get_by_email("grace@example.com") is user
    assert repository.exists("grace@example.com") is True
    assert repository.exists("missing@example.com") is False

    user.full_name = "Rear Admiral Grace Hopper"
    updated_user = repository.update(user)
    assert updated_user.full_name == "Rear Admiral Grace Hopper"

    repository.delete(user)
    assert repository.get_by_id(user.id) is None
    session.close()
