"""Unit tests for the Purchase SQLAlchemy model."""

from datetime import datetime, timezone
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models.purchase import PaymentStatus, Purchase
from app.models.vehicle import FuelType, TransmissionType, Vehicle, VehicleCondition


def create_test_session() -> Session:
    """Return an isolated in-memory database session."""
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def build_vehicle() -> Vehicle:
    """Build a valid vehicle for a purchase relationship."""
    return Vehicle(
        manufacturer="Toyota",
        model="Corolla",
        vin="1HGCM82633A004352",
        year=2024,
        purchase_price=Decimal("18000.00"),
        selling_price=Decimal("22000.00"),
        color="Silver",
        mileage=0,
        fuel_type=FuelType.PETROL,
        transmission=TransmissionType.AUTOMATIC,
        condition=VehicleCondition.NEW,
    )


def build_purchase(vehicle: Vehicle, **overrides: object) -> Purchase:
    """Build a valid vehicle-acquisition record."""
    attributes: dict[str, object] = {
        "vehicle": vehicle,
        "supplier_name": "Northstar Motors",
        "purchase_price": Decimal("18000.00"),
        "purchase_date": datetime(2026, 7, 19, tzinfo=timezone.utc),
        "invoice_number": "INV-1001",
    }
    attributes.update(overrides)
    return Purchase(**attributes)  # type: ignore[arg-type]


def test_purchase_model_assigns_defaults_timestamps_and_relationship() -> None:
    session = create_test_session()
    vehicle = build_vehicle()
    purchase = build_purchase(vehicle)
    session.add(purchase)
    session.commit()
    session.refresh(purchase)

    assert purchase.id is not None
    assert purchase.payment_status is PaymentStatus.PENDING
    assert purchase.vehicle is vehicle
    assert vehicle.purchase is purchase
    assert purchase.created_at is not None
    assert purchase.updated_at is not None
    session.close()


def test_purchase_model_enforces_positive_price_and_unique_fields() -> None:
    session = create_test_session()
    first_vehicle = build_vehicle()
    session.add(build_purchase(first_vehicle, purchase_price=Decimal("0.00")))
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

    first_purchase = build_purchase(first_vehicle)
    session.add(first_purchase)
    session.commit()
    second_vehicle = build_vehicle()
    second_vehicle.vin = "1HGCM82633A004353"
    session.add(build_purchase(second_vehicle))
    with pytest.raises(IntegrityError):
        session.commit()
    session.close()


def test_purchase_model_enforces_one_purchase_per_vehicle() -> None:
    session = create_test_session()
    vehicle = build_vehicle()
    session.add(build_purchase(vehicle))
    session.commit()
    session.add(
        Purchase(
            vehicle_id=vehicle.id,
            supplier_name="Northstar Motors",
            purchase_price=Decimal("18500.00"),
            purchase_date=datetime(2026, 7, 19, tzinfo=timezone.utc),
            invoice_number="INV-1002",
        )
    )

    with pytest.raises(IntegrityError):
        session.commit()
    session.close()
