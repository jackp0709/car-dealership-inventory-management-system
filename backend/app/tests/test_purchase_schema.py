"""Unit tests for Purchase Pydantic schemas."""

from datetime import datetime, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.models.purchase import PaymentStatus
from app.schemas.purchase import PurchaseCreate, PurchaseUpdate


def valid_purchase_payload() -> dict[str, object]:
    """Return a valid vehicle-acquisition payload."""
    return {
        "vehicle_id": 1,
        "supplier_name": "Northstar Motors",
        "purchase_price": "18000.00",
        "purchase_date": datetime(2026, 7, 19, tzinfo=timezone.utc),
        "invoice_number": "INV-1001",
    }


def test_purchase_create_accepts_valid_payload_and_default_payment_status() -> None:
    purchase = PurchaseCreate(**valid_purchase_payload())

    assert purchase.purchase_price == Decimal("18000.00")
    assert purchase.payment_status is PaymentStatus.PENDING
    assert purchase.notes is None


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("vehicle_id", 0),
        ("supplier_name", ""),
        ("purchase_price", "0.00"),
        ("invoice_number", ""),
        ("payment_status", "PARTIAL"),
    ],
)
def test_purchase_create_rejects_invalid_values(field: str, value: object) -> None:
    payload = valid_purchase_payload()
    payload[field] = value

    with pytest.raises(ValidationError):
        PurchaseCreate(**payload)


def test_purchase_update_rejects_immutable_and_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        PurchaseUpdate(vehicle_id=1)

    with pytest.raises(ValidationError):
        PurchaseUpdate(purchase_price="18000.00")
