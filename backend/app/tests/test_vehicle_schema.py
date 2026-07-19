"""Unit tests for Vehicle Pydantic schemas."""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.models.vehicle import FuelType, TransmissionType, VehicleCondition
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


def valid_vehicle_payload() -> dict[str, object]:
    """Return a valid vehicle creation payload."""
    return {
        "manufacturer": "Toyota",
        "model": "Corolla",
        "vin": "1HGCM82633A004352",
        "year": 2024,
        "purchase_price": "18000.00",
        "selling_price": "22000.00",
        "color": "Silver",
        "mileage": 0,
        "fuel_type": "HYBRID",
        "transmission": "AUTOMATIC",
        "condition": "NEW",
    }


def test_vehicle_create_accepts_valid_payload_and_optional_description() -> None:
    vehicle = VehicleCreate(**valid_vehicle_payload())

    assert vehicle.description is None
    assert vehicle.purchase_price == Decimal("18000.00")
    assert vehicle.fuel_type is FuelType.HYBRID
    assert vehicle.transmission is TransmissionType.AUTOMATIC
    assert vehicle.condition is VehicleCondition.NEW


def test_vehicle_create_rejects_missing_required_fields() -> None:
    payload = valid_vehicle_payload()
    payload.pop("manufacturer")

    with pytest.raises(ValidationError):
        VehicleCreate(**payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("year", 3000),
        ("purchase_price", "0.00"),
        ("selling_price", "-1.00"),
        ("mileage", -1),
        ("fuel_type", "HYDROGEN"),
        ("transmission", "CVT"),
        ("condition", "CERTIFIED"),
    ],
)
def test_vehicle_create_rejects_invalid_values(field: str, value: object) -> None:
    payload = valid_vehicle_payload()
    payload[field] = value

    with pytest.raises(ValidationError):
        VehicleCreate(**payload)


def test_vehicle_update_rejects_immutable_and_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        VehicleUpdate(vin="1HGCM82633A004352")

    with pytest.raises(ValidationError):
        VehicleUpdate(status="SOLD")
