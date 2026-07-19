"""SQLAlchemy persistence model for dealership staff users."""

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SqlAlchemyEnum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class UserRole(str, Enum):
    """Supported dealership staff roles."""

    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"


class User(Base):
    """Persisted dealership staff account."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SqlAlchemyEnum(UserRole, name="user_role", native_enum=True, create_constraint=True),
        nullable=False,
        default=UserRole.EMPLOYEE,
        server_default=UserRole.EMPLOYEE.value,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
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
    sales: Mapped[list["Sale"]] = relationship(back_populates="seller")


import app.models.sale  # noqa: E402, F401
