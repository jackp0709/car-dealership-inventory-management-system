"""Database access operations for Sale records."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.purchase import Purchase
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

    def get_count(self) -> int:
        """Return the total number of completed sales."""
        return int(self._session.scalar(select(func.count(Sale.id))))

    def get_total_sales_revenue(self) -> Decimal:
        """Return the total revenue from recorded sales."""
        statement = select(func.coalesce(func.sum(Sale.sale_price), 0))
        return Decimal(self._session.scalar(statement))

    def get_estimated_gross_profit(self) -> Decimal:
        """Return realized gross profit for sales with recorded acquisition costs."""
        statement = select(
            func.coalesce(func.sum(Sale.sale_price - Purchase.purchase_price), 0)
        ).join(Purchase, Purchase.vehicle_id == Sale.vehicle_id)
        return Decimal(self._session.scalar(statement))

    def get_recent_activity_records(
        self,
        limit: int,
    ) -> list[tuple[int, int, str, datetime]]:
        """Return recently recorded sales in descending creation order."""
        statement = (
            select(Sale.id, Sale.vehicle_id, Sale.customer_name, Sale.created_at)
            .order_by(Sale.created_at.desc(), Sale.id.desc())
            .limit(limit)
        )
        return list(self._session.execute(statement).tuples())

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
