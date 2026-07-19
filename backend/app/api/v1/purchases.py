"""Versioned Purchase CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.models.purchase import Purchase
from app.models.user import User
from app.repositories.purchase_repository import PurchaseRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.purchase import PurchaseCreate, PurchaseRead, PurchaseUpdate


router = APIRouter()


def _purchase_not_found() -> HTTPException:
    """Return the standard missing-purchase response."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found.")


@router.post("", response_model=PurchaseRead, status_code=status.HTTP_201_CREATED)
def create_purchase(
    payload: PurchaseCreate,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> Purchase:
    """Record a vehicle acquisition."""
    purchase_repository = PurchaseRepository(session)
    if VehicleRepository(session).get_by_id(payload.vehicle_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found.")
    if purchase_repository.get_by_vehicle_id(payload.vehicle_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vehicle already has a purchase.",
        )
    if purchase_repository.get_by_invoice_number(payload.invoice_number) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invoice number already exists.",
        )

    try:
        purchase = purchase_repository.create(Purchase(**payload.model_dump()))
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Purchase conflicts with an existing vehicle or invoice.",
        ) from error
    return purchase


@router.get("", response_model=list[PurchaseRead])
def list_purchases(
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> list[Purchase]:
    """Return all vehicle acquisition records without pagination."""
    return PurchaseRepository(session).get_all()


@router.get("/{purchase_id}", response_model=PurchaseRead)
def get_purchase(
    purchase_id: int,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> Purchase:
    """Return a vehicle acquisition by identifier."""
    purchase = PurchaseRepository(session).get_by_id(purchase_id)
    if purchase is None:
        raise _purchase_not_found()
    return purchase


@router.put("/{purchase_id}", response_model=PurchaseRead)
def update_purchase(
    purchase_id: int,
    payload: PurchaseUpdate,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> Purchase:
    """Update the supported vehicle-acquisition attributes."""
    repository = PurchaseRepository(session)
    purchase = repository.get_by_id(purchase_id)
    if purchase is None:
        raise _purchase_not_found()

    updates = payload.model_dump(exclude_unset=True)
    invoice_number = updates.get("invoice_number")
    if (
        invoice_number is not None
        and invoice_number != purchase.invoice_number
        and repository.get_by_invoice_number(invoice_number) is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invoice number already exists.",
        )

    for field, value in updates.items():
        setattr(purchase, field, value)

    try:
        updated_purchase = repository.update(purchase)
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invoice number already exists.",
        ) from error
    return updated_purchase


@router.delete("/{purchase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase(
    purchase_id: int,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> Response:
    """Delete a vehicle acquisition record."""
    repository = PurchaseRepository(session)
    purchase = repository.get_by_id(purchase_id)
    if purchase is None:
        raise _purchase_not_found()
    repository.delete(purchase)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
