"""Tests for JWT authentication behavior."""

from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.auth import router as auth_router
from app.core.auth import (
    create_access_token,
    get_current_user,
    verify_token,
)
from app.core.config import get_settings
from app.core.dependencies import get_db
from app.core.security import hash_password
from app.database.base import Base
from app.models.user import User


def create_auth_test_client() -> tuple[TestClient, Session]:
    """Create an application client backed by an isolated database."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = Session(engine)
    application = FastAPI()
    application.include_router(auth_router, prefix="/api/v1/auth")

    @application.get("/protected")
    def protected_route(current_user: User = Depends(get_current_user)) -> dict[str, int]:
        return {"id": current_user.id}

    application.dependency_overrides[get_db] = lambda: session
    return TestClient(application), session


def create_user(session: Session) -> User:
    """Persist a user suitable for authentication tests."""
    user = User(
        full_name="Ada Lovelace",
        email="ada@example.com",
        hashed_password=hash_password("correct-horse-battery-staple"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_login_returns_access_token_for_valid_credentials() -> None:
    client, session = create_auth_test_client()
    create_user(session)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "ada@example.com", "password": "correct-horse-battery-staple"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]
    session.close()


@pytest.mark.parametrize(
    ("email", "password"),
    [
        ("ada@example.com", "incorrect-password"),
        ("unknown@example.com", "correct-horse-battery-staple"),
    ],
)
def test_login_rejects_invalid_credentials(email: str, password: str) -> None:
    client, session = create_auth_test_client()
    create_user(session)

    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password."
    session.close()


def test_access_token_contains_subject_and_is_validated() -> None:
    token = create_access_token(42)

    payload = verify_token(token)

    assert payload["sub"] == "42"
    assert "exp" in payload


def test_verify_token_rejects_expired_tokens() -> None:
    settings = get_settings()
    expired_token = jwt.encode(
        {"sub": "42", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(HTTPException) as exception_info:
        verify_token(expired_token)

    assert exception_info.value.status_code == 401


def test_current_user_dependency_resolves_bearer_token() -> None:
    client, session = create_auth_test_client()
    user = create_user(session)
    token = create_access_token(user.id)

    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {"id": user.id}
    session.close()


def test_current_user_dependency_rejects_invalid_token() -> None:
    client, session = create_auth_test_client()

    response = client.get("/protected", headers={"Authorization": "Bearer invalid-token"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials."
    session.close()


def test_inactive_user_cannot_log_in_or_access_protected_routes() -> None:
    client, session = create_auth_test_client()
    user = create_user(session)
    user.is_active = False
    session.commit()

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "ada@example.com", "password": "correct-horse-battery-staple"},
    )
    protected_response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {create_access_token(user.id)}"},
    )

    assert login_response.status_code == 401
    assert protected_response.status_code == 401
    session.close()
