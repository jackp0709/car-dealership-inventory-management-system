"""SQLAlchemy persistence model for dealership vehicle acquisitions."""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SqlAlchemyEnum,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class PaymentStatus(str, Enum):
    """Supported payment states for a vehicle acquisition."""

    PENDING = "PENDING"
    PAID = "PAID"


class Purchase(Base):
    """Persisted record of a dealership vehicle acquisition."""

    __tablename__ = "purchase"
    __table_args__ = (
        CheckConstraint("purchase_price > 0", name="purchase_price_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicle.id", ondelete="RESTRICT"),
        unique=True,
        nullable=False,
    )
    supplier_name: Mapped[str] = mapped_column(String(255), nullable=False)
    purchase_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    purchase_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    invoice_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    payment_status: Mapped[PaymentStatus] = mapped_column(
        SqlAlchemyEnum(
            PaymentStatus,
            name="purchase_payment_status",
            native_enum=True,
            create_constraint=True,
        ),
        nullable=False,
        default=PaymentStatus.PENDING,
        server_default=PaymentStatus.PENDING.value,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
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
    vehicle: Mapped["Vehicle"] = relationship(back_populates="purchase")


import app.models.vehicle  # noqa: E402, F401
