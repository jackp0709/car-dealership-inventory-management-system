"""Unit tests for the Vehicle SQLAlchemy model."""

from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models.vehicle import (
    FuelType,
    TransmissionType,
    Vehicle,
    VehicleCondition,
    VehicleStatus,
)


def create_test_session() -> Session:
    """Return an isolated in-memory database session."""
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def build_vehicle(**overrides: object) -> Vehicle:
    """Build a valid vehicle with optional field overrides."""
    attributes: dict[str, object] = {
        "manufacturer": "Toyota",
        "model": "Corolla",
        "vin": "1HGCM82633A004352",
        "year": 2024,
        "purchase_price": Decimal("18000.00"),
        "selling_price": Decimal("22000.00"),
        "color": "Silver",
        "mileage": 0,
        "fuel_type": FuelType.PETROL,
        "transmission": TransmissionType.AUTOMATIC,
        "condition": VehicleCondition.NEW,
    }
    attributes.update(overrides)
    return Vehicle(**attributes)  # type: ignore[arg-type]


def test_vehicle_model_assigns_defaults_and_timestamps() -> None:
    session = create_test_session()
    vehicle = build_vehicle()

    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)

    assert vehicle.id is not None
    assert vehicle.status is VehicleStatus.AVAILABLE
    assert vehicle.purchase_price == Decimal("18000.00")
    assert vehicle.selling_price == Decimal("22000.00")
    assert vehicle.created_at is not None
    assert vehicle.updated_at is not None
    session.close()


def test_vehicle_model_supports_documented_enum_values() -> None:
    assert {fuel_type.value for fuel_type in FuelType} == {
        "PETROL",
        "DIESEL",
        "CNG",
        "ELECTRIC",
        "HYBRID",
    }
    assert {transmission.value for transmission in TransmissionType} == {
        "MANUAL",
        "AUTOMATIC",
    }
    assert {condition.value for condition in VehicleCondition} == {"NEW", "USED"}
    assert {status.value for status in VehicleStatus} == {"AVAILABLE", "SOLD"}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("mileage", -1),
        ("purchase_price", Decimal("0.00")),
        ("selling_price", Decimal("-1.00")),
    ],
)
def test_vehicle_model_enforces_database_check_constraints(field: str, value: object) -> None:
    session = create_test_session()
    vehicle = build_vehicle(**{field: value})
    session.add(vehicle)

    with pytest.raises(IntegrityError):
        session.commit()
    session.close()


def test_vehicle_model_enforces_unique_vin() -> None:
    session = create_test_session()
    session.add(build_vehicle())
    session.commit()
    session.add(build_vehicle(model="Camry"))

    with pytest.raises(IntegrityError):
        session.commit()
    session.close()
