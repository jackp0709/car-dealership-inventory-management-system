"""Unit tests for Sale Pydantic schemas."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.sale import SaleCreate, SaleUpdate


def valid_sale_payload() -> dict[str, object]:
    """Return a valid vehicle-sale payload."""
    return {
        "vehicle_id": 1,
        "seller_id": 1,
        "customer_name": "Grace Hopper",
        "customer_email": "grace@example.com",
        "customer_phone": "+15551234567",
        "sale_price": "22000.00",
        "sale_date": datetime.now(timezone.utc),
    }


def test_sale_create_accepts_valid_payload() -> None:
    sale = SaleCreate(**valid_sale_payload())

    assert sale.sale_price == Decimal("22000.00")
    assert sale.customer_email == "grace@example.com"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("vehicle_id", 0),
        ("seller_id", 0),
        ("customer_name", ""),
        ("customer_email", "not-an-email"),
        ("customer_phone", ""),
        ("sale_price", "0.00"),
    ],
)
def test_sale_create_rejects_invalid_values(field: str, value: object) -> None:
    payload = valid_sale_payload()
    payload[field] = value

    with pytest.raises(ValidationError):
        SaleCreate(**payload)


def test_sale_create_rejects_future_sale_date() -> None:
    payload = valid_sale_payload()
    payload["sale_date"] = datetime.now(timezone.utc) + timedelta(days=1)

    with pytest.raises(ValidationError, match="Sale date cannot be in the future"):
        SaleCreate(**payload)


def test_sale_update_rejects_immutable_and_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        SaleUpdate(vehicle_id=1)

    with pytest.raises(ValidationError):
        SaleUpdate(sale_price="22000.00")
