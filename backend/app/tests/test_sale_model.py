"""Unit tests for the Sale SQLAlchemy model."""

from datetime import datetime, timezone
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models.sale import Sale
from app.models.user import User
from app.models.vehicle import FuelType, TransmissionType, Vehicle, VehicleCondition


def create_test_session() -> Session:
    """Return an isolated in-memory database session."""
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def build_vehicle(vin: str = "1HGCM82633A004352") -> Vehicle:
    """Build a valid vehicle for a sale relationship."""
    return Vehicle(
        manufacturer="Toyota",
        model="Corolla",
        vin=vin,
        year=2024,
        purchase_price=Decimal("18000.00"),
        selling_price=Decimal("22000.00"),
        color="Silver",
        mileage=0,
        fuel_type=FuelType.PETROL,
        transmission=TransmissionType.AUTOMATIC,
        condition=VehicleCondition.NEW,
    )


def build_seller() -> User:
    """Build a valid dealership employee for a sale relationship."""
    return User(
        full_name="Ada Lovelace",
        email="ada@example.com",
        hashed_password="hashed-value",
    )


def build_sale(vehicle: Vehicle, seller: User, **overrides: object) -> Sale:
    """Build a valid sale with optional field overrides."""
    attributes: dict[str, object] = {
        "vehicle": vehicle,
        "seller": seller,
        "customer_name": "Grace Hopper",
        "customer_email": "grace@example.com",
        "customer_phone": "+15551234567",
        "sale_price": Decimal("22000.00"),
        "sale_date": datetime(2026, 7, 19, tzinfo=timezone.utc),
    }
    attributes.update(overrides)
    return Sale(**attributes)  # type: ignore[arg-type]


def test_sale_model_assigns_timestamps_and_bidirectional_relationships() -> None:
    session = create_test_session()
    vehicle = build_vehicle()
    seller = build_seller()
    sale = build_sale(vehicle, seller)
    session.add(sale)
    session.commit()
    session.refresh(sale)

    assert sale.id is not None
    assert sale.vehicle is vehicle
    assert vehicle.sale is sale
    assert sale.seller is seller
    assert seller.sales == [sale]
    assert sale.created_at is not None
    assert sale.updated_at is not None
    session.close()


def test_sale_model_enforces_positive_price_and_one_sale_per_vehicle() -> None:
    session = create_test_session()
    vehicle = build_vehicle()
    seller = build_seller()
    session.add(build_sale(vehicle, seller, sale_price=Decimal("0.00")))
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

    first_sale = build_sale(
        build_vehicle("1HGCM82633A004353"),
        User(
            full_name="Alan Turing",
            email="alan@example.com",
            hashed_password="hashed-value",
        ),
    )
    session.add(first_sale)
    session.commit()
    session.add(
        Sale(
            vehicle_id=vehicle.id,
            seller_id=seller.id,
            customer_name="Barbara Liskov",
            customer_email="barbara@example.com",
            customer_phone="+15557654321",
            sale_price=Decimal("22100.00"),
            sale_date=datetime(2026, 7, 19, tzinfo=timezone.utc),
        )
    )
    with pytest.raises(IntegrityError):
        session.commit()
    session.close()
