"""Versioned user CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate


router = APIRouter()
_optional_bearer_scheme = HTTPBearer(auto_error=False)


def _user_not_found() -> HTTPException:
    """Return the standard missing-user response."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


def _current_user_for_creation(
    session: Session,
    repository: UserRepository,
    credentials: HTTPAuthorizationCredentials | None,
) -> User | None:
    """Allow bootstrap creation only while the user table is empty."""
    if not repository.get_all():
        return None
    return get_current_user(credentials=credentials, session=session)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    credentials: HTTPAuthorizationCredentials | None = Depends(_optional_bearer_scheme),
    session: Session = Depends(get_db),
) -> User:
    """Create the initial user publicly or later users with JWT authentication."""
    repository = UserRepository(session)
    _current_user_for_creation(session, repository, credentials)

    if repository.exists(payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists.")

    try:
        user = repository.create(
            User(
                full_name=payload.full_name,
                email=payload.email,
                hashed_password=hash_password(payload.password),
                role=payload.role,
            )
        )
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        ) from error
    return user


@router.get("", response_model=list[UserRead])
def list_users(
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> list[User]:
    """Return all users without exposing password hashes."""
    return UserRepository(session).get_all()


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> User:
    """Return a user by identifier."""
    user = UserRepository(session).get_by_id(user_id)
    if user is None:
        raise _user_not_found()
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> User:
    """Update the supported user attributes."""
    repository = UserRepository(session)
    user = repository.get_by_id(user_id)
    if user is None:
        raise _user_not_found()

    updates = payload.model_dump(exclude_unset=True)
    email = updates.get("email")
    if email is not None and email != user.email and repository.exists(email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists.")

    for field, value in updates.items():
        setattr(user, field, value)

    try:
        updated_user = repository.update(user)
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        ) from error
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> Response:
    """Permanently delete a user."""
    repository = UserRepository(session)
    user = repository.get_by_id(user_id)
    if user is None:
        raise _user_not_found()
    repository.delete(user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
