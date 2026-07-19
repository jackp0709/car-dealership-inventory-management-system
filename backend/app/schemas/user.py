"""Pydantic schemas for user data exchange."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class UserBase(BaseModel):
    """Shared user attributes accepted from trusted application layers."""

    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    role: UserRole = UserRole.EMPLOYEE


class UserCreate(UserBase):
    """Attributes required to create a user before password hashing."""

    password: str = Field(min_length=8, max_length=72)


class UserUpdate(BaseModel):
    """Mutable user attributes."""

    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserRead(UserBase):
    """Safe user representation that excludes password hashes."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
