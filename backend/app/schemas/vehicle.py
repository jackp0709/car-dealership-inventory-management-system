"""Pydantic schemas for vehicle data exchange."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.vehicle import FuelType, TransmissionType, VehicleCondition, VehicleStatus


class VehicleBase(BaseModel):
    """Shared vehicle attributes accepted from trusted application layers."""

    manufacturer: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=100)
    vin: str = Field(min_length=1, max_length=17)
    year: int = Field(ge=1886, le=date.today().year)
    purchase_price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    selling_price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    color: str = Field(min_length=1, max_length=30)
    mileage: int = Field(ge=0)
    fuel_type: FuelType
    transmission: TransmissionType
    condition: VehicleCondition
    description: str | None = None


class VehicleCreate(VehicleBase):
    """Attributes required to add a vehicle to inventory."""


class VehicleUpdate(BaseModel):
    """Mutable vehicle attributes excluding VIN and lifecycle status."""

    model_config = ConfigDict(extra="forbid")

    manufacturer: str | None = Field(default=None, min_length=1, max_length=50)
    model: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=1886, le=date.today().year)
    purchase_price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )
    selling_price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )
    color: str | None = Field(default=None, min_length=1, max_length=30)
    mileage: int | None = Field(default=None, ge=0)
    fuel_type: FuelType | None = None
    transmission: TransmissionType | None = None
    condition: VehicleCondition | None = None
    description: str | None = None


class VehicleRead(VehicleBase):
    """Vehicle representation returned from persistence."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    status: VehicleStatus
    created_at: datetime
    updated_at: datetime
