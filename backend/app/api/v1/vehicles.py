"""Versioned vehicle CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, require_admin
from app.core.dependencies import get_db
from app.models.user import User
from app.models.vehicle import Vehicle, VehicleStatus
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import VehicleCreate, VehicleRead, VehicleUpdate


router = APIRouter()


def _vehicle_not_found() -> HTTPException:
    """Return the standard missing-vehicle response."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found.")


@router.post("", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate,
    _: User = Depends(require_admin),
    session: Session = Depends(get_db),
) -> Vehicle:
    """Add a vehicle to inventory."""
    try:
        vehicle = VehicleRepository(session).create(Vehicle(**payload.model_dump()))
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="VIN already exists.",
        ) from error
    return vehicle


@router.get("", response_model=list[VehicleRead])
def list_vehicles(
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> list[Vehicle]:
    """Return all vehicles without pagination."""
    return VehicleRepository(session).get_all()


@router.get("/{vehicle_id}", response_model=VehicleRead)
def get_vehicle(
    vehicle_id: int,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> Vehicle:
    """Return a vehicle by identifier."""
    vehicle = VehicleRepository(session).get_by_id(vehicle_id)
    if vehicle is None:
        raise _vehicle_not_found()
    return vehicle


@router.put("/{vehicle_id}", response_model=VehicleRead)
def update_vehicle(
    vehicle_id: int,
    payload: VehicleUpdate,
    _: User = Depends(require_admin),
    session: Session = Depends(get_db),
) -> Vehicle:
    """Update the supported vehicle attributes."""
    repository = VehicleRepository(session)
    vehicle = repository.get_by_id(vehicle_id)
    if vehicle is None:
        raise _vehicle_not_found()

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(vehicle, field, value)

    updated_vehicle = repository.update(vehicle)
    session.commit()
    return updated_vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: int,
    _: User = Depends(require_admin),
    session: Session = Depends(get_db),
) -> Response:
    """Permanently delete an available vehicle."""
    repository = VehicleRepository(session)
    vehicle = repository.get_by_id(vehicle_id)
    if vehicle is None:
        raise _vehicle_not_found()
    if vehicle.status is VehicleStatus.SOLD:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sold vehicles cannot be deleted.",
        )

    repository.delete(vehicle)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
