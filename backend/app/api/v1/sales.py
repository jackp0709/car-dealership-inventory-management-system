"""Versioned Sale CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, require_admin
from app.core.dependencies import get_db
from app.models.sale import Sale
from app.models.user import User, UserRole
from app.models.vehicle import VehicleStatus
from app.repositories.sale_repository import SaleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.sale import SaleCreate, SaleRead, SaleUpdate


router = APIRouter()


def _sale_not_found() -> HTTPException:
    """Return the standard missing-sale response."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found.")


@router.post("", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(
    payload: SaleCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> Sale:
    """Record a sale and atomically mark its vehicle as sold."""
    if current_user.role is UserRole.EMPLOYEE and payload.seller_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employees can record sales only for themselves.",
        )
    sale_repository = SaleRepository(session)
    vehicle_repository = VehicleRepository(session)
    vehicle = vehicle_repository.get_by_id(payload.vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found.")
    if vehicle.status is not VehicleStatus.AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vehicle is not available for sale.",
        )
    if sale_repository.get_by_vehicle_id(payload.vehicle_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vehicle already has a sale.",
        )
    if UserRepository(session).get_by_id(payload.seller_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found.")

    try:
        sale = sale_repository.create(Sale(**payload.model_dump()))
        vehicle.status = VehicleStatus.SOLD
        vehicle_repository.update(vehicle)
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sale conflicts with an existing vehicle or seller.",
        ) from error
    except SQLAlchemyError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not record sale.",
        ) from error
    return sale


@router.get("", response_model=list[SaleRead])
def list_sales(
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> list[Sale]:
    """Return all sales without pagination."""
    return SaleRepository(session).get_all()


@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(
    sale_id: int,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> Sale:
    """Return a sale by identifier."""
    sale = SaleRepository(session).get_by_id(sale_id)
    if sale is None:
        raise _sale_not_found()
    return sale


@router.put("/{sale_id}", response_model=SaleRead)
def update_sale(
    sale_id: int,
    payload: SaleUpdate,
    _: User = Depends(require_admin),
    session: Session = Depends(get_db),
) -> Sale:
    """Update customer details without altering inventory history."""
    repository = SaleRepository(session)
    sale = repository.get_by_id(sale_id)
    if sale is None:
        raise _sale_not_found()

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(sale, field, value)

    try:
        updated_sale = repository.update(sale)
        session.commit()
    except SQLAlchemyError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update sale.",
        ) from error
    return updated_sale


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(
    sale_id: int,
    _: User = Depends(require_admin),
    session: Session = Depends(get_db),
) -> Response:
    """Delete a sale and atomically return its vehicle to available inventory."""
    sale_repository = SaleRepository(session)
    sale = sale_repository.get_by_id(sale_id)
    if sale is None:
        raise _sale_not_found()

    vehicle = VehicleRepository(session).get_by_id(sale.vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found.")

    try:
        sale_repository.delete(sale)
        vehicle.status = VehicleStatus.AVAILABLE
        VehicleRepository(session).update(vehicle)
        session.commit()
    except SQLAlchemyError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not delete sale.",
        ) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
