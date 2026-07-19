"""Unit tests for the Purchase repository."""

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models.purchase import Purchase
from app.models.vehicle import FuelType, TransmissionType, Vehicle, VehicleCondition
from app.repositories.purchase_repository import PurchaseRepository


def create_test_session() -> Session:
    """Return an isolated in-memory database session."""
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def build_vehicle(vin: str) -> Vehicle:
    """Build a valid vehicle for a purchase relationship."""
    return Vehicle(
        manufacturer="Toyota",
        model="Corolla",
        vin=vin,
        year=2024,
        purchase_price=Decimal("18000.00"),
        selling_price=Decimal("22000.00"),
        color="Silver",
        mileage=0,
        fuel_type=FuelType.PETROL,
        transmission=TransmissionType.AUTOMATIC,
        condition=VehicleCondition.NEW,
    )


def build_purchase(vehicle: Vehicle, invoice_number: str) -> Purchase:
    """Build a valid vehicle-acquisition record."""
    return Purchase(
        vehicle=vehicle,
        supplier_name="Northstar Motors",
        purchase_price=Decimal("18000.00"),
        purchase_date=datetime(2026, 7, 19, tzinfo=timezone.utc),
        invoice_number=invoice_number,
    )


def test_purchase_repository_crud_operations() -> None:
    session = create_test_session()
    repository = PurchaseRepository(session)
    first_purchase = repository.create(build_purchase(build_vehicle("1HGCM82633A004352"), "INV-1001"))
    second_purchase = repository.create(build_purchase(build_vehicle("1HGCM82633A004353"), "INV-1002"))

    assert repository.get_by_id(first_purchase.id) is first_purchase
    assert repository.get_by_vehicle_id(first_purchase.vehicle_id) is first_purchase
    assert repository.get_all() == [first_purchase, second_purchase]

    first_purchase.supplier_name = "Updated Motors"
    assert repository.update(first_purchase).supplier_name == "Updated Motors"

    repository.delete(second_purchase)
    assert repository.get_by_id(second_purchase.id) is None
    session.close()
