"""Database access operations for Vehicle records."""

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle, VehicleStatus


class VehicleRepository:
    """Encapsulate persistence operations for vehicles."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, vehicle: Vehicle) -> Vehicle:
        """Add a vehicle to the current database transaction."""
        self._session.add(vehicle)
        self._session.flush()
        self._session.refresh(vehicle)
        return vehicle

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        """Return a vehicle by primary key, if present."""
        return self._session.get(Vehicle, vehicle_id)

    def get_all(self) -> list[Vehicle]:
        """Return all vehicles ordered by primary key."""
        statement = select(Vehicle).order_by(Vehicle.id)
        return list(self._session.scalars(statement))

    def get_operational_counts(self) -> tuple[int, int, int]:
        """Return total, available, and sold inventory counts in one query."""
        statement = select(
            func.count(Vehicle.id),
            func.coalesce(
                func.sum(case((Vehicle.status == VehicleStatus.AVAILABLE, 1), else_=0)),
                0,
            ),
            func.coalesce(
                func.sum(case((Vehicle.status == VehicleStatus.SOLD, 1), else_=0)),
                0,
            ),
        )
        total, available, sold = self._session.execute(statement).one()
        return int(total), int(available), int(sold)

    def update(self, vehicle: Vehicle) -> Vehicle:
        """Flush changes to an existing vehicle in the current transaction."""
        self._session.add(vehicle)
        self._session.flush()
        self._session.refresh(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        """Delete a vehicle from the current database transaction."""
        self._session.delete(vehicle)
        self._session.flush()
