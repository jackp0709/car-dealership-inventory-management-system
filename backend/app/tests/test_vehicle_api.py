"""Tests for authenticated vehicle CRUD endpoints."""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.vehicles import router as vehicles_router
from app.core.auth import create_access_token
from app.core.dependencies import get_db
from app.core.security import hash_password
from app.database.base import Base
from app.models.user import User
from app.models.vehicle import Vehicle, VehicleStatus


def create_vehicles_test_client() -> tuple[TestClient, Session]:
    """Create an API client backed by an isolated database."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = Session(engine)
    application = FastAPI()
    application.include_router(vehicles_router, prefix="/api/v1/vehicles")
    application.dependency_overrides[get_db] = lambda: session
    return TestClient(application), session


def create_user(session: Session) -> User:
    """Persist a user that can authenticate endpoint requests."""
    user = User(
        full_name="Ada Lovelace",
        email="ada@example.com",
        hashed_password=hash_password("correct-horse-battery-staple"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authorization_header(user: User) -> dict[str, str]:
    """Return a valid Bearer header for the supplied user."""
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


def vehicle_payload(vin: str = "1HGCM82633A004352") -> dict[str, object]:
    """Return a valid vehicle creation payload."""
    return {
        "manufacturer": "Toyota",
        "model": "Corolla",
        "vin": vin,
        "year": 2024,
        "purchase_price": "18000.00",
        "selling_price": "22000.00",
        "color": "Silver",
        "mileage": 0,
        "fuel_type": "HYBRID",
        "transmission": "AUTOMATIC",
        "condition": "NEW",
        "description": "Hybrid sedan",
    }


def test_vehicle_endpoints_require_authentication() -> None:
    client, session = create_vehicles_test_client()

    assert client.post("/api/v1/vehicles", json=vehicle_payload()).status_code == 401
    assert client.get("/api/v1/vehicles").status_code == 401
    assert client.get("/api/v1/vehicles/1").status_code == 401
    assert client.put("/api/v1/vehicles/1", json={"color": "Blue"}).status_code == 401
    assert client.delete("/api/v1/vehicles/1").status_code == 401
    session.close()


def test_create_and_list_vehicles() -> None:
    client, session = create_vehicles_test_client()
    headers = authorization_header(create_user(session))

    create_response = client.post("/api/v1/vehicles", headers=headers, json=vehicle_payload())
    list_response = client.get("/api/v1/vehicles", headers=headers)

    assert create_response.status_code == 201
    assert create_response.json()["vin"] == "1HGCM82633A004352"
    assert create_response.json()["status"] == "AVAILABLE"
    assert list_response.status_code == 200
    assert [vehicle["vin"] for vehicle in list_response.json()] == ["1HGCM82633A004352"]
    session.close()


def test_create_vehicle_rejects_invalid_payload_and_duplicate_vin() -> None:
    client, session = create_vehicles_test_client()
    headers = authorization_header(create_user(session))

    invalid_response = client.post(
        "/api/v1/vehicles",
        headers=headers,
        json={**vehicle_payload(), "mileage": -1},
    )
    first_response = client.post("/api/v1/vehicles", headers=headers, json=vehicle_payload())
    duplicate_response = client.post("/api/v1/vehicles", headers=headers, json=vehicle_payload())

    assert invalid_response.status_code == 422
    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
    assert duplicate_response.json()["detail"] == "VIN already exists."
    session.close()


def test_get_and_update_vehicle_and_reject_missing_vehicle() -> None:
    client, session = create_vehicles_test_client()
    headers = authorization_header(create_user(session))
    created_vehicle = client.post("/api/v1/vehicles", headers=headers, json=vehicle_payload()).json()

    get_response = client.get(f"/api/v1/vehicles/{created_vehicle['id']}", headers=headers)
    update_response = client.put(
        f"/api/v1/vehicles/{created_vehicle['id']}",
        headers=headers,
        json={"color": "Blue", "mileage": 250},
    )
    missing_response = client.get("/api/v1/vehicles/9999", headers=headers)
    invalid_id_response = client.get("/api/v1/vehicles/not-an-id", headers=headers)

    assert get_response.status_code == 200
    assert get_response.json()["id"] == created_vehicle["id"]
    assert update_response.status_code == 200
    assert update_response.json()["color"] == "Blue"
    assert update_response.json()["mileage"] == 250
    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "Vehicle not found."
    assert invalid_id_response.status_code == 422
    session.close()


def test_update_vehicle_rejects_invalid_payload_and_missing_vehicle() -> None:
    client, session = create_vehicles_test_client()
    headers = authorization_header(create_user(session))
    created_vehicle = client.post("/api/v1/vehicles", headers=headers, json=vehicle_payload()).json()

    invalid_response = client.put(
        f"/api/v1/vehicles/{created_vehicle['id']}",
        headers=headers,
        json={"selling_price": 0},
    )
    missing_response = client.put(
        "/api/v1/vehicles/9999",
        headers=headers,
        json={"color": "Blue"},
    )

    assert invalid_response.status_code == 422
    assert missing_response.status_code == 404
    session.close()


def test_delete_available_vehicle_and_reject_missing_vehicle() -> None:
    client, session = create_vehicles_test_client()
    headers = authorization_header(create_user(session))
    created_vehicle = client.post("/api/v1/vehicles", headers=headers, json=vehicle_payload()).json()

    delete_response = client.delete(f"/api/v1/vehicles/{created_vehicle['id']}", headers=headers)
    missing_response = client.delete(f"/api/v1/vehicles/{created_vehicle['id']}", headers=headers)

    assert delete_response.status_code == 204
    assert missing_response.status_code == 404
    session.close()


def test_delete_sold_vehicle_is_rejected() -> None:
    client, session = create_vehicles_test_client()
    headers = authorization_header(create_user(session))
    created_vehicle = client.post("/api/v1/vehicles", headers=headers, json=vehicle_payload()).json()
    vehicle = session.get(Vehicle, created_vehicle["id"])
    assert vehicle is not None
    vehicle.status = VehicleStatus.SOLD
    session.commit()

    response = client.delete(f"/api/v1/vehicles/{created_vehicle['id']}", headers=headers)

    assert response.status_code == 409
    assert response.json()["detail"] == "Sold vehicles cannot be deleted."
    assert session.get(Vehicle, created_vehicle["id"]) is not None
    session.close()
