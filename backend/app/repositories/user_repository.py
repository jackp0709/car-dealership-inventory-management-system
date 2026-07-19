"""Database access operations for User records."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Encapsulate persistence operations for users."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, user: User) -> User:
        """Add a user to the current database transaction."""
        self._session.add(user)
        self._session.flush()
        self._session.refresh(user)
        return user

    def get_all(self) -> list[User]:
        """Return all users ordered by primary key."""
        statement = select(User).order_by(User.id)
        return list(self._session.scalars(statement))

    def get_by_id(self, user_id: int) -> User | None:
        """Return a user by primary key, if present."""
        return self._session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        """Return a user by email, if present."""
        statement = select(User).where(User.email == email)
        return self._session.scalar(statement)

    def exists(self, email: str) -> bool:
        """Return whether a user exists with the supplied email."""
        statement = select(User.id).where(User.email == email).limit(1)
        return self._session.scalar(statement) is not None

    def update(self, user: User) -> User:
        """Flush changes to an existing user in the current transaction."""
        self._session.add(user)
        self._session.flush()
        self._session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Delete a user from the current database transaction."""
        self._session.delete(user)
        self._session.flush()
