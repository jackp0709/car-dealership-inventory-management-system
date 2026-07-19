"""JWT authentication utilities and request dependency."""

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.dependencies import get_db
from app.core.security import verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenData


_bearer_scheme = HTTPBearer(auto_error=False)
_invalid_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    """Return the user when the supplied credentials are valid."""
    user = UserRepository(session).get_by_email(email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(subject: int) -> str:
    """Create a signed access token with configured expiration."""
    settings = get_settings()
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    payload = {"sub": str(subject), "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> dict[str, Any]:
    """Validate a JWT and return its claims or raise a generic 401 error."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["sub", "exp"]},
        )
    except InvalidTokenError as error:
        raise _invalid_credentials_exception from error

    subject = payload.get("sub")
    try:
        TokenData(user_id=int(subject))
    except (TypeError, ValueError):
        raise _invalid_credentials_exception from None
    return payload


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    session: Session = Depends(get_db),
) -> User:
    """Resolve the current user from a valid Bearer access token."""
    if credentials is None:
        raise _invalid_credentials_exception

    payload = verify_token(credentials.credentials)
    user = UserRepository(session).get_by_id(int(payload["sub"]))
    if user is None:
        raise _invalid_credentials_exception
    return user
