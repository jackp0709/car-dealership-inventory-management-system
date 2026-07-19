"""Database access operations for Purchase records."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.purchase import Purchase


class PurchaseRepository:
    """Encapsulate persistence operations for vehicle acquisitions."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, purchase: Purchase) -> Purchase:
        """Add a purchase to the current database transaction."""
        self._session.add(purchase)
        self._session.flush()
        self._session.refresh(purchase)
        return purchase

    def get_by_id(self, purchase_id: int) -> Purchase | None:
        """Return a purchase by primary key, if present."""
        return self._session.get(Purchase, purchase_id)

    def get_by_vehicle_id(self, vehicle_id: int) -> Purchase | None:
        """Return the acquisition record associated with a vehicle, if present."""
        statement = select(Purchase).where(Purchase.vehicle_id == vehicle_id)
        return self._session.scalar(statement)

    def get_by_invoice_number(self, invoice_number: str) -> Purchase | None:
        """Return a purchase by supplier invoice number, if present."""
        statement = select(Purchase).where(Purchase.invoice_number == invoice_number)
        return self._session.scalar(statement)

    def get_all(self) -> list[Purchase]:
        """Return all purchases ordered by primary key."""
        statement = select(Purchase).order_by(Purchase.id)
        return list(self._session.scalars(statement))

    def update(self, purchase: Purchase) -> Purchase:
        """Flush changes to an existing purchase in the current transaction."""
        self._session.add(purchase)
        self._session.flush()
        self._session.refresh(purchase)
        return purchase

    def delete(self, purchase: Purchase) -> None:
        """Delete a purchase from the current database transaction."""
        self._session.delete(purchase)
        self._session.flush()
