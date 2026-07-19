"""Tests for authenticated Sale CRUD endpoints and inventory processing."""

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1 import sales as sales_api
from app.api.v1.sales import router as sales_router
from app.core.auth import create_access_token
from app.core.dependencies import get_db
from app.core.security import hash_password
from app.database.base import Base
from app.models.sale import Sale
from app.models.user import User, UserRole
from app.models.vehicle import FuelType, TransmissionType, Vehicle, VehicleCondition, VehicleStatus
from app.repositories.vehicle_repository import VehicleRepository


def create_sales_test_client() -> tuple[TestClient, Session]:
    """Create an API client backed by an isolated database."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = Session(engine)
    application = FastAPI()
    application.include_router(sales_router, prefix="/api/v1/sales")
    application.dependency_overrides[get_db] = lambda: session
    return TestClient(application), session


def create_user(
    session: Session,
    email: str = "ada@example.com",
    role: UserRole = UserRole.ADMIN,
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
    """Persist a valid vehicle available for sale."""
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


def sale_payload(vehicle_id: int, seller_id: int) -> dict[str, object]:
    """Return a valid vehicle-sale payload."""
    return {
        "vehicle_id": vehicle_id,
        "seller_id": seller_id,
        "customer_name": "Grace Hopper",
        "customer_email": "grace@example.com",
        "customer_phone": "+15551234567",
        "sale_price": "22000.00",
        "sale_date": "2026-07-19T10:00:00Z",
    }


def test_sale_endpoints_require_authentication() -> None:
    client, session = create_sales_test_client()

    assert client.post("/api/v1/sales", json=sale_payload(1, 1)).status_code == 401
    assert client.get("/api/v1/sales").status_code == 401
    assert client.get("/api/v1/sales/1").status_code == 401
    assert client.put("/api/v1/sales/1", json={"customer_name": "Updated"}).status_code == 401
    assert client.delete("/api/v1/sales/1").status_code == 401
    assert client.get(
        "/api/v1/sales",
        headers={"Authorization": "Bearer invalid-token"},
    ).status_code == 401
    session.close()


def test_create_list_and_get_sale_updates_vehicle_inventory() -> None:
    client, session = create_sales_test_client()
    seller = create_user(session)
    vehicle = create_vehicle(session)
    headers = authorization_header(seller)

    create_response = client.post(
        "/api/v1/sales",
        headers=headers,
        json=sale_payload(vehicle.id, seller.id),
    )
    list_response = client.get("/api/v1/sales", headers=headers)
    get_response = client.get(f"/api/v1/sales/{create_response.json()['id']}", headers=headers)

    assert create_response.status_code == 201
    assert create_response.json()["vehicle_id"] == vehicle.id
    assert create_response.json()["sale_price"] == "22000.00"
    assert session.get(Vehicle, vehicle.id).status is VehicleStatus.SOLD
    assert list_response.status_code == 200
    assert [sale["id"] for sale in list_response.json()] == [create_response.json()["id"]]
    assert get_response.status_code == 200
    assert get_response.json()["seller_id"] == seller.id
    session.close()


def test_create_sale_rejects_invalid_references_and_duplicate_sales() -> None:
    client, session = create_sales_test_client()
    seller = create_user(session)
    vehicle = create_vehicle(session)
    headers = authorization_header(seller)

    first_response = client.post(
        "/api/v1/sales",
        headers=headers,
        json=sale_payload(vehicle.id, seller.id),
    )
    duplicate_response = client.post(
        "/api/v1/sales",
        headers=headers,
        json=sale_payload(vehicle.id, seller.id),
    )
    missing_vehicle_response = client.post(
        "/api/v1/sales",
        headers=headers,
        json=sale_payload(9999, seller.id),
    )
    other_vehicle = create_vehicle(session, "1HGCM82633A004353")
    missing_seller_response = client.post(
        "/api/v1/sales",
        headers=headers,
        json=sale_payload(other_vehicle.id, 9999),
    )
    invalid_payload_response = client.post(
        "/api/v1/sales",
        headers=headers,
        json={**sale_payload(other_vehicle.id, seller.id), "sale_price": "0.00"},
    )

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
    assert duplicate_response.json()["detail"] == "Vehicle is not available for sale."
    assert missing_vehicle_response.status_code == 404
    assert missing_seller_response.status_code == 404
    assert invalid_payload_response.status_code == 422
    session.close()


def test_update_delete_and_missing_sale_preserve_inventory_consistency() -> None:
    client, session = create_sales_test_client()
    seller = create_user(session)
    vehicle = create_vehicle(session)
    headers = authorization_header(seller)
    sale_id = client.post(
        "/api/v1/sales",
        headers=headers,
        json=sale_payload(vehicle.id, seller.id),
    ).json()["id"]

    update_response = client.put(
        f"/api/v1/sales/{sale_id}",
        headers=headers,
        json={"customer_name": "Rear Admiral Grace Hopper"},
    )
    immutable_response = client.put(
        f"/api/v1/sales/{sale_id}",
        headers=headers,
        json={"vehicle_id": vehicle.id},
    )
    delete_response = client.delete(f"/api/v1/sales/{sale_id}", headers=headers)
    missing_response = client.get(f"/api/v1/sales/{sale_id}", headers=headers)

    assert update_response.status_code == 200
    assert update_response.json()["customer_name"] == "Rear Admiral Grace Hopper"
    assert immutable_response.status_code == 422
    assert delete_response.status_code == 204
    assert session.get(Sale, sale_id) is None
    assert session.get(Vehicle, vehicle.id).status is VehicleStatus.AVAILABLE
    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "Sale not found."
    session.close()


def test_create_sale_rolls_back_when_inventory_update_fails(monkeypatch: object) -> None:
    client, session = create_sales_test_client()
    seller = create_user(session)
    vehicle = create_vehicle(session)
    headers = authorization_header(seller)

    def fail_update(self: VehicleRepository, vehicle: Vehicle) -> Vehicle:
        del self, vehicle
        raise SQLAlchemyError("Simulated inventory failure")

    monkeypatch.setattr(sales_api.VehicleRepository, "update", fail_update)  # type: ignore[attr-defined]
    response = client.post(
        "/api/v1/sales",
        headers=headers,
        json=sale_payload(vehicle.id, seller.id),
    )

    assert response.status_code == 500
    assert session.query(Sale).count() == 0
    assert session.get(Vehicle, vehicle.id).status is VehicleStatus.AVAILABLE
    session.close()


def test_employee_can_record_only_their_own_sales() -> None:
    client, session = create_sales_test_client()
    employee = create_user(session, role=UserRole.EMPLOYEE)
    other_employee = create_user(session, "grace@example.com", role=UserRole.EMPLOYEE)
    own_vehicle = create_vehicle(session)
    other_vehicle = create_vehicle(session, "1HGCM82633A004353")
    headers = authorization_header(employee)

    own_sale_response = client.post(
        "/api/v1/sales",
        headers=headers,
        json=sale_payload(own_vehicle.id, employee.id),
    )
    impersonated_sale_response = client.post(
        "/api/v1/sales",
        headers=headers,
        json=sale_payload(other_vehicle.id, other_employee.id),
    )
    update_response = client.put(
        f"/api/v1/sales/{own_sale_response.json()['id']}",
        headers=headers,
        json={"customer_name": "Updated"},
    )

    assert own_sale_response.status_code == 201
    assert impersonated_sale_response.status_code == 403
    assert update_response.status_code == 403
    session.close()
