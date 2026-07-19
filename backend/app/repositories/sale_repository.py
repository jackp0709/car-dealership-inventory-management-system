"""Database access operations for Sale records."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sale import Sale


class SaleRepository:
    """Encapsulate persistence operations for completed vehicle sales."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, sale: Sale) -> Sale:
        """Add a sale to the current database transaction."""
        self._session.add(sale)
        self._session.flush()
        self._session.refresh(sale)
        return sale

    def get_by_id(self, sale_id: int) -> Sale | None:
        """Return a sale by primary key, if present."""
        return self._session.get(Sale, sale_id)

    def get_by_vehicle_id(self, vehicle_id: int) -> Sale | None:
        """Return the sale associated with a vehicle, if present."""
        statement = select(Sale).where(Sale.vehicle_id == vehicle_id)
        return self._session.scalar(statement)

    def get_all(self) -> list[Sale]:
        """Return all sales ordered by primary key."""
        statement = select(Sale).order_by(Sale.id)
        return list(self._session.scalars(statement))

    def update(self, sale: Sale) -> Sale:
        """Flush changes to an existing sale in the current transaction."""
        self._session.add(sale)
        self._session.flush()
        self._session.refresh(sale)
        return sale

    def delete(self, sale: Sale) -> None:
        """Delete a sale from the current database transaction."""
        self._session.delete(sale)
        self._session.flush()
