"""Versioned authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import authenticate_user, create_access_token
from app.core.dependencies import get_db
from app.schemas.auth import LoginRequest, Token


router = APIRouter()


@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, session: Session = Depends(get_db)) -> Token:
    """Authenticate a user and return a JWT access token."""
    user = authenticate_user(session, credentials.email, credentials.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user.id))
