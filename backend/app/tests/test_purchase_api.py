"""Tests for authenticated Purchase CRUD endpoints."""

from datetime import date, timedelta

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.purchases import router as purchases_router
from app.core.auth import create_access_token
from app.core.dependencies import get_db
from app.core.security import hash_password
from app.database.base import Base
from app.models.user import User, UserRole
from app.models.vehicle import FuelType, TransmissionType, Vehicle, VehicleCondition


def create_purchases_test_client() -> tuple[TestClient, Session]:
    """Create an API client backed by an isolated database."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = Session(engine)
    application = FastAPI()
    application.include_router(purchases_router, prefix="/api/v1/purchases")
    application.dependency_overrides[get_db] = lambda: session
    return TestClient(application), session


def create_user(
    session: Session,
    role: UserRole = UserRole.ADMIN,
    email: str = "ada@example.com",
) -> User:
    """Persist a user that can authenticate endpoint requests."""
    user = User(
        full_name="Ada Lovelace",
        email=email,
        hashed_password=hash_password("correct-horse-battery-staple"),
        role=role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_vehicle(session: Session, vin: str = "1HGCM82633A004352") -> Vehicle:
    """Persist a valid vehicle available for a Purchase record."""
    vehicle = Vehicle(
        manufacturer="Toyota",
        model="Corolla",
        vin=vin,
        year=2024,
        purchase_price="18000.00",
        selling_price="22000.00",
        color="Silver",
        mileage=0,
        fuel_type=FuelType.HYBRID,
        transmission=TransmissionType.AUTOMATIC,
        condition=VehicleCondition.NEW,
    )
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle


def authorization_header(user: User) -> dict[str, str]:
    """Return a valid Bearer header for the supplied user."""
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


def purchase_payload(vehicle_id: int, invoice_number: str = "INV-1001") -> dict[str, object]:
    """Return a valid vehicle-acquisition payload."""
    return {
        "vehicle_id": vehicle_id,
        "supplier_name": "Northstar Motors",
        "purchase_price": "18000.00",
        "purchase_date": "2026-07-19T10:00:00Z",
        "invoice_number": invoice_number,
        "payment_status": "PENDING",
        "notes": "First acquisition",
    }


def test_purchase_endpoints_require_authentication() -> None:
    client, session = create_purchases_test_client()

    assert client.post("/api/v1/purchases", json=purchase_payload(1)).status_code == 401
    assert client.get("/api/v1/purchases").status_code == 401
    assert client.get("/api/v1/purchases/1").status_code == 401
    assert client.put("/api/v1/purchases/1", json={"notes": "Updated"}).status_code == 401
    assert client.delete("/api/v1/purchases/1").status_code == 401
    session.close()


def test_create_list_and_get_purchase() -> None:
    client, session = create_purchases_test_client()
    headers = authorization_header(create_user(session))
    vehicle = create_vehicle(session)

    create_response = client.post("/api/v1/purchases", headers=headers, json=purchase_payload(vehicle.id))
    list_response = client.get("/api/v1/purchases", headers=headers)
    get_response = client.get(
        f"/api/v1/purchases/{create_response.json()['id']}",
        headers=headers,
    )

    assert create_response.status_code == 201
    assert create_response.json()["invoice_number"] == "INV-1001"
    assert list_response.status_code == 200
    assert [purchase["id"] for purchase in list_response.json()] == [create_response.json()["id"]]
    assert get_response.status_code == 200
    assert get_response.json()["vehicle_id"] == vehicle.id
    session.close()


def test_create_purchase_rejects_invalid_vehicle_duplicates_and_invalid_data() -> None:
    client, session = create_purchases_test_client()
    headers = authorization_header(create_user(session))
    vehicle = create_vehicle(session)
    first_response = client.post("/api/v1/purchases", headers=headers, json=purchase_payload(vehicle.id))
    duplicate_vehicle_response = client.post(
        "/api/v1/purchases",
        headers=headers,
        json=purchase_payload(vehicle.id, "INV-1002"),
    )
    other_vehicle = create_vehicle(session, "1HGCM82633A004353")
    duplicate_invoice_response = client.post(
        "/api/v1/purchases",
        headers=headers,
        json=purchase_payload(other_vehicle.id),
    )
    missing_vehicle_response = client.post(
        "/api/v1/purchases",
        headers=headers,
        json=purchase_payload(9999, "INV-1003"),
    )
    future_date_response = client.post(
        "/api/v1/purchases",
        headers=headers,
        json={
            **purchase_payload(other_vehicle.id, "INV-1004"),
            "purchase_date": (date.today() + timedelta(days=1)).isoformat(),
        },
    )
    invalid_price_response = client.post(
        "/api/v1/purchases",
        headers=headers,
        json={**purchase_payload(other_vehicle.id, "INV-1005"), "purchase_price": "0.00"},
    )

    assert first_response.status_code == 201
    assert duplicate_vehicle_response.status_code == 409
    assert duplicate_vehicle_response.json()["detail"] == "Vehicle already has a purchase."
    assert duplicate_invoice_response.status_code == 409
    assert duplicate_invoice_response.json()["detail"] == "Invoice number already exists."
    assert missing_vehicle_response.status_code == 404
    assert future_date_response.status_code == 422
    assert invalid_price_response.status_code == 422
    session.close()


def test_update_and_delete_purchase_and_reject_missing_purchase() -> None:
    client, session = create_purchases_test_client()
    headers = authorization_header(create_user(session))
    vehicle = create_vehicle(session)
    purchase_id = client.post(
        "/api/v1/purchases",
        headers=headers,
        json=purchase_payload(vehicle.id),
    ).json()["id"]

    update_response = client.put(
        f"/api/v1/purchases/{purchase_id}",
        headers=headers,
        json={"supplier_name": "Updated Motors", "payment_status": "PAID"},
    )
    delete_response = client.delete(f"/api/v1/purchases/{purchase_id}", headers=headers)
    missing_response = client.get(f"/api/v1/purchases/{purchase_id}", headers=headers)
    invalid_id_response = client.get("/api/v1/purchases/not-an-id", headers=headers)

    assert update_response.status_code == 200
    assert update_response.json()["supplier_name"] == "Updated Motors"
    assert update_response.json()["payment_status"] == "PAID"
    assert delete_response.status_code == 204
    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "Purchase not found."
    assert invalid_id_response.status_code == 422
    session.close()


def test_update_rejects_duplicate_invoice_and_immutable_fields() -> None:
    client, session = create_purchases_test_client()
    headers = authorization_header(create_user(session))
    first_vehicle = create_vehicle(session)
    second_vehicle = create_vehicle(session, "1HGCM82633A004353")
    first_id = client.post(
        "/api/v1/purchases",
        headers=headers,
        json=purchase_payload(first_vehicle.id, "INV-1001"),
    ).json()["id"]
    second_id = client.post(
        "/api/v1/purchases",
        headers=headers,
        json=purchase_payload(second_vehicle.id, "INV-1002"),
    ).json()["id"]

    duplicate_response = client.put(
        f"/api/v1/purchases/{second_id}",
        headers=headers,
        json={"invoice_number": "INV-1001"},
    )
    immutable_response = client.put(
        f"/api/v1/purchases/{first_id}",
        headers=headers,
        json={"vehicle_id": second_vehicle.id},
    )

    assert duplicate_response.status_code == 409
    assert immutable_response.status_code == 422
    session.close()


def test_employee_can_view_but_cannot_change_purchases() -> None:
    client, session = create_purchases_test_client()
    administrator_headers = authorization_header(create_user(session))
    employee_headers = authorization_header(
        create_user(session, role=UserRole.EMPLOYEE, email="employee@example.com")
    )
    vehicle = create_vehicle(session)
    purchase_id = client.post(
        "/api/v1/purchases",
        headers=administrator_headers,
        json=purchase_payload(vehicle.id),
    ).json()["id"]

    assert client.get("/api/v1/purchases", headers=employee_headers).status_code == 200
    assert client.get(f"/api/v1/purchases/{purchase_id}", headers=employee_headers).status_code == 200
    assert client.post(
        "/api/v1/purchases",
        headers=employee_headers,
        json=purchase_payload(vehicle.id, "INV-1002"),
    ).status_code == 403
    assert client.put(
        f"/api/v1/purchases/{purchase_id}", headers=employee_headers, json={"notes": "Updated"}
    ).status_code == 403
    assert client.delete(f"/api/v1/purchases/{purchase_id}", headers=employee_headers).status_code == 403
    session.close()
