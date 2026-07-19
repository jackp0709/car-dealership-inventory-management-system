"""Tests for authenticated dashboard aggregation endpoints."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.dashboard import router as dashboard_router
from app.core.auth import create_access_token
from app.core.dependencies import get_db
from app.core.security import hash_password
from app.database.base import Base
from app.models.purchase import Purchase
from app.models.sale import Sale
from app.models.user import User
from app.models.vehicle import FuelType, TransmissionType, Vehicle, VehicleCondition, VehicleStatus


def create_dashboard_test_client() -> tuple[TestClient, Session]:
    """Return an API client backed by an isolated database."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = Session(engine)
    application = FastAPI()
    application.include_router(dashboard_router, prefix="/api/v1/dashboard")
    application.dependency_overrides[get_db] = lambda: session
    return TestClient(application), session


def create_user(session: Session) -> User:
    """Persist a user eligible to access protected endpoints."""
    user = User(
        full_name="Ada Lovelace",
        email="ada@example.com",
        hashed_password=hash_password("correct-horse-battery-staple"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_vehicle(session: Session, vin: str, status: VehicleStatus) -> Vehicle:
    """Persist a valid inventory vehicle with the supplied lifecycle status."""
    vehicle = Vehicle(
        manufacturer="Toyota",
        model="Corolla",
        vin=vin,
        year=2024,
        purchase_price=Decimal("18000.00"),
        selling_price=Decimal("22000.00"),
        color="Silver",
        mileage=0,
        fuel_type=FuelType.HYBRID,
        transmission=TransmissionType.AUTOMATIC,
        condition=VehicleCondition.NEW,
        status=status,
    )
    session.add(vehicle)
    session.flush()
    return vehicle


def authorization_header(user: User) -> dict[str, str]:
    """Return a valid bearer authorization header."""
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


def seed_dashboard_data(session: Session, user: User) -> tuple[Purchase, Purchase, Sale]:
    """Create representative inventory, acquisition, and sale records."""
    start = datetime(2026, 7, 19, 8, 0, tzinfo=timezone.utc)
    sold_vehicle = create_vehicle(session, "1HGCM82633A004352", VehicleStatus.SOLD)
    purchased_vehicle = create_vehicle(session, "1HGCM82633A004353", VehicleStatus.AVAILABLE)
    create_vehicle(session, "1HGCM82633A004354", VehicleStatus.AVAILABLE)
    purchase = Purchase(
        vehicle_id=sold_vehicle.id,
        supplier_name="Northstar Motors",
        purchase_price=Decimal("18000.00"),
        purchase_date=start,
        invoice_number="INV-1001",
        created_at=start,
    )
    second_purchase = Purchase(
        vehicle_id=purchased_vehicle.id,
        supplier_name="City Motors",
        purchase_price=Decimal("15000.00"),
        purchase_date=start + timedelta(hours=1),
        invoice_number="INV-1002",
        created_at=start + timedelta(hours=1),
    )
    sale = Sale(
        vehicle_id=sold_vehicle.id,
        seller_id=user.id,
        customer_name="Grace Hopper",
        customer_email="grace@example.com",
        customer_phone="+15551234567",
        sale_price=Decimal("22000.00"),
        sale_date=start + timedelta(hours=2),
        created_at=start + timedelta(hours=2),
    )
    session.add_all([purchase, second_purchase, sale])
    session.commit()
    return purchase, second_purchase, sale


def test_dashboard_endpoints_require_authentication() -> None:
    client, session = create_dashboard_test_client()

    for path in ("/summary", "/operational-metrics", "/financial-metrics", "/recent-activity"):
        assert client.get(f"/api/v1/dashboard{path}").status_code == 401

    session.close()


def test_dashboard_summary_and_individual_metrics_are_accurate() -> None:
    client, session = create_dashboard_test_client()
    user = create_user(session)
    purchase, second_purchase, sale = seed_dashboard_data(session, user)
    headers = authorization_header(user)

    summary_response = client.get("/api/v1/dashboard/summary", headers=headers)
    operational_response = client.get("/api/v1/dashboard/operational-metrics", headers=headers)
    financial_response = client.get("/api/v1/dashboard/financial-metrics", headers=headers)
    activity_response = client.get("/api/v1/dashboard/recent-activity", headers=headers)

    expected_operational = {
        "total_vehicles": 3,
        "available_vehicles": 2,
        "sold_vehicles": 1,
        "total_purchases": 2,
        "total_completed_sales": 1,
    }
    expected_financial = {
        "total_purchase_cost": "33000.00",
        "total_sales_revenue": "22000.00",
        "estimated_gross_profit": "4000.00",
    }

    assert summary_response.status_code == 200
    assert summary_response.json()["operational_metrics"] == expected_operational
    assert summary_response.json()["financial_metrics"] == expected_financial
    assert operational_response.json() == expected_operational
    assert financial_response.json() == expected_financial
    assert activity_response.status_code == 200
    assert activity_response.json()["activities"][:2] == [
        {
            "activity_type": "SALE",
            "record_id": sale.id,
            "vehicle_id": sale.vehicle_id,
            "counterparty_name": "Grace Hopper",
            "recorded_at": "2026-07-19T10:00:00",
        },
        {
            "activity_type": "PURCHASE",
            "record_id": second_purchase.id,
            "vehicle_id": second_purchase.vehicle_id,
            "counterparty_name": "City Motors",
            "recorded_at": "2026-07-19T09:00:00",
        },
    ]
    session.close()
