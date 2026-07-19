"""Unit tests for the Vehicle repository."""

from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models.vehicle import FuelType, TransmissionType, Vehicle, VehicleCondition
from app.repositories.vehicle_repository import VehicleRepository


def create_test_session() -> Session:
    """Return an isolated in-memory database session."""
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def build_vehicle(vin: str, model: str = "Corolla") -> Vehicle:
    """Build a valid vehicle for repository tests."""
    return Vehicle(
        manufacturer="Toyota",
        model=model,
        vin=vin,
        year=2024,
        purchase_price=Decimal("18000.00"),
        selling_price=Decimal("22000.00"),
        color="Silver",
        mileage=0,
        fuel_type=FuelType.HYBRID,
        transmission=TransmissionType.AUTOMATIC,
        condition=VehicleCondition.NEW,
    )


def test_vehicle_repository_creates_and_retrieves_vehicles() -> None:
    session = create_test_session()
    repository = VehicleRepository(session)
    first_vehicle = repository.create(build_vehicle("1HGCM82633A004352"))
    second_vehicle = repository.create(build_vehicle("1HGCM82633A004353", "Camry"))

    assert repository.get_by_id(first_vehicle.id) is first_vehicle
    assert repository.get_by_id(9999) is None
    assert repository.get_all() == [first_vehicle, second_vehicle]
    session.close()


def test_vehicle_repository_updates_and_deletes_vehicle() -> None:
    session = create_test_session()
    repository = VehicleRepository(session)
    vehicle = repository.create(build_vehicle("1HGCM82633A004352"))

    vehicle.color = "Blue"
    updated_vehicle = repository.update(vehicle)
    assert updated_vehicle.color == "Blue"

    repository.delete(updated_vehicle)
    assert repository.get_by_id(updated_vehicle.id) is None
    session.close()
