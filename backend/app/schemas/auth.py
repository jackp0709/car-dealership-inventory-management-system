"""Pydantic schemas for authentication data exchange."""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Credentials accepted by the login endpoint."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Access token returned after successful authentication."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Validated JWT claims required to identify a user."""

    user_id: int
