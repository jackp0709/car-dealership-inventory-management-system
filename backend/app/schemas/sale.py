"""Pydantic schemas for vehicle sale data exchange."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class SaleBase(BaseModel):
    """Shared vehicle sale attributes."""

    customer_name: str = Field(min_length=1, max_length=255)
    customer_email: EmailStr
    customer_phone: str = Field(min_length=1, max_length=20)
    sale_price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    sale_date: datetime

    @field_validator("sale_date")
    @classmethod
    def sale_date_must_not_be_in_the_future(cls, value: datetime) -> datetime:
        """Reject sales dated after the current calendar date."""
        if value.date() > date.today():
            raise ValueError("Sale date cannot be in the future.")
        return value


class SaleCreate(SaleBase):
    """Attributes required to record a vehicle sale."""

    vehicle_id: int = Field(gt=0)
    seller_id: int = Field(gt=0)


class SaleUpdate(BaseModel):
    """Mutable sale attributes that do not alter its vehicle or seller."""

    model_config = ConfigDict(extra="forbid")

    customer_name: str | None = Field(default=None, min_length=1, max_length=255)
    customer_email: EmailStr | None = None
    customer_phone: str | None = Field(default=None, min_length=1, max_length=20)


class SaleRead(SaleBase):
    """Sale representation returned from persistence."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: int
    seller_id: int
    created_at: datetime
    updated_at: datetime
