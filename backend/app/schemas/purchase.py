"""Pydantic schemas for vehicle acquisition data exchange."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.purchase import PaymentStatus


class PurchaseBase(BaseModel):
    """Shared vehicle acquisition attributes."""

    supplier_name: str = Field(min_length=1, max_length=255)
    purchase_price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    purchase_date: datetime
    invoice_number: str = Field(min_length=1, max_length=100)
    payment_status: PaymentStatus = PaymentStatus.PENDING
    notes: str | None = None


class PurchaseCreate(PurchaseBase):
    """Attributes required to record a vehicle acquisition."""

    vehicle_id: int = Field(gt=0)


class PurchaseUpdate(BaseModel):
    """Mutable vehicle acquisition attributes."""

    model_config = ConfigDict(extra="forbid")

    supplier_name: str | None = Field(default=None, min_length=1, max_length=255)
    invoice_number: str | None = Field(default=None, min_length=1, max_length=100)
    payment_status: PaymentStatus | None = None
    notes: str | None = None


class PurchaseRead(PurchaseBase):
    """Purchase representation returned from persistence."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: int
    created_at: datetime
    updated_at: datetime
