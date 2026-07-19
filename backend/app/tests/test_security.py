"""Unit tests for password security helpers."""

from app.core.security import hash_password, verify_password


def test_hash_password_does_not_store_plaintext() -> None:
    password = "correct-horse-battery-staple"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert hashed_password.startswith("$2")


def test_verify_password_accepts_only_the_matching_password() -> None:
    hashed_password = hash_password("correct-horse-battery-staple")

    assert verify_password("correct-horse-battery-staple", hashed_password) is True
    assert verify_password("incorrect-password", hashed_password) is False
