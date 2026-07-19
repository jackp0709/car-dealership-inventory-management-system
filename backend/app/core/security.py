"""Password hashing and verification helpers."""

from passlib.context import CryptContext


_password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return a bcrypt hash for a plaintext password."""
    return _password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Return whether a plaintext password matches its bcrypt hash."""
    return _password_context.verify(password, hashed_password)
