"""SQLAlchemy persistence model for completed vehicle sales."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Sale(Base):
    """Persisted record of a vehicle sale and its customer details."""

    __tablename__ = "sale"
    __table_args__ = (
        CheckConstraint("sale_price > 0", name="sale_price_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicle.id", ondelete="RESTRICT"),
        unique=True,
        nullable=False,
    )
    seller_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    sale_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    sale_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
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
    vehicle: Mapped["Vehicle"] = relationship(back_populates="sale")
    seller: Mapped["User"] = relationship(back_populates="sales")


import app.models.user  # noqa: E402, F401
import app.models.vehicle  # noqa: E402, F401
