"""Tests for authenticated user CRUD endpoints."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.users import router as users_router
from app.core.auth import create_access_token
from app.core.dependencies import get_db
from app.core.security import hash_password
from app.database.base import Base
from app.models.user import User


def create_users_test_client() -> tuple[TestClient, Session]:
    """Create an API client backed by an isolated database."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = Session(engine)
    application = FastAPI()
    application.include_router(users_router, prefix="/api/v1/users")
    application.dependency_overrides[get_db] = lambda: session
    return TestClient(application), session


def create_user(session: Session, email: str, full_name: str) -> User:
    """Persist a user for endpoint tests."""
    user = User(
        full_name=full_name,
        email=email,
        hashed_password=hash_password("correct-horse-battery-staple"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authorization_header(user: User) -> dict[str, str]:
    """Return a valid Bearer header for the supplied user."""
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


def test_list_users_requires_authentication() -> None:
    client, session = create_users_test_client()

    response = client.get("/api/v1/users")

    assert response.status_code == 401
    session.close()


def test_list_and_get_user() -> None:
    client, session = create_users_test_client()
    current_user = create_user(session, "ada@example.com", "Ada Lovelace")
    second_user = create_user(session, "grace@example.com", "Grace Hopper")
    headers = authorization_header(current_user)

    list_response = client.get("/api/v1/users", headers=headers)
    get_response = client.get(f"/api/v1/users/{second_user.id}", headers=headers)

    assert list_response.status_code == 200
    assert [user["email"] for user in list_response.json()] == [
        "ada@example.com",
        "grace@example.com",
    ]
    assert get_response.status_code == 200
    assert "hashed_password" not in get_response.json()
    assert get_response.json()["id"] == second_user.id
    session.close()


def test_update_user_and_reject_duplicate_email() -> None:
    client, session = create_users_test_client()
    current_user = create_user(session, "ada@example.com", "Ada Lovelace")
    target_user = create_user(session, "grace@example.com", "Grace Hopper")
    headers = authorization_header(current_user)

    update_response = client.put(
        f"/api/v1/users/{target_user.id}",
        headers=headers,
        json={"full_name": "Rear Admiral Grace Hopper"},
    )
    duplicate_response = client.put(
        f"/api/v1/users/{target_user.id}",
        headers=headers,
        json={"email": "ada@example.com"},
    )

    assert update_response.status_code == 200
    assert update_response.json()["full_name"] == "Rear Admiral Grace Hopper"
    assert duplicate_response.status_code == 409
    assert duplicate_response.json()["detail"] == "Email already exists."
    session.close()


def test_delete_user_and_reject_missing_user() -> None:
    client, session = create_users_test_client()
    current_user = create_user(session, "ada@example.com", "Ada Lovelace")
    target_user = create_user(session, "grace@example.com", "Grace Hopper")
    headers = authorization_header(current_user)

    delete_response = client.delete(f"/api/v1/users/{target_user.id}", headers=headers)
    missing_response = client.get(f"/api/v1/users/{target_user.id}", headers=headers)
    invalid_id_response = client.get("/api/v1/users/not-an-id", headers=headers)

    assert delete_response.status_code == 204
    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "User not found."
    assert invalid_id_response.status_code == 422
    session.close()
