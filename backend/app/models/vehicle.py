"""SQLAlchemy persistence model for dealership inventory vehicles."""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SqlAlchemyEnum,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class FuelType(str, Enum):
    """Supported vehicle fuel types."""

    PETROL = "PETROL"
    DIESEL = "DIESEL"
    CNG = "CNG"
    ELECTRIC = "ELECTRIC"
    HYBRID = "HYBRID"


class TransmissionType(str, Enum):
    """Supported vehicle transmission types."""

    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"


class VehicleCondition(str, Enum):
    """Supported vehicle conditions."""

    NEW = "NEW"
    USED = "USED"


class VehicleStatus(str, Enum):
    """Supported vehicle inventory statuses."""

    AVAILABLE = "AVAILABLE"
    SOLD = "SOLD"


class Vehicle(Base):
    """Persisted dealership inventory vehicle."""

    __tablename__ = "vehicle"
    __table_args__ = (
        CheckConstraint("mileage >= 0", name="mileage_non_negative"),
        CheckConstraint("purchase_price > 0", name="purchase_price_positive"),
        CheckConstraint("selling_price > 0", name="selling_price_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    vin: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    purchase_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    selling_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    color: Mapped[str] = mapped_column(String(30), nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    fuel_type: Mapped[FuelType] = mapped_column(
        SqlAlchemyEnum(FuelType, name="fuel_type", native_enum=True, create_constraint=True),
        nullable=False,
    )
    transmission: Mapped[TransmissionType] = mapped_column(
        SqlAlchemyEnum(
            TransmissionType,
            name="transmission_type",
            native_enum=True,
            create_constraint=True,
        ),
        nullable=False,
    )
    condition: Mapped[VehicleCondition] = mapped_column(
        SqlAlchemyEnum(
            VehicleCondition,
            name="vehicle_condition",
            native_enum=True,
            create_constraint=True,
        ),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[VehicleStatus] = mapped_column(
        SqlAlchemyEnum(
            VehicleStatus,
            name="vehicle_status",
            native_enum=True,
            create_constraint=True,
        ),
        nullable=False,
        default=VehicleStatus.AVAILABLE,
        server_default=VehicleStatus.AVAILABLE.value,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    purchase: Mapped["Purchase | None"] = relationship(
        back_populates="vehicle",
        uselist=False,
    )
    sale: Mapped["Sale | None"] = relationship(
        back_populates="vehicle",
        uselist=False,
    )


import app.models.purchase  # noqa: E402, F401
import app.models.sale  # noqa: E402, F401
