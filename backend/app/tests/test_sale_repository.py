"""Unit tests for the Sale repository."""

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models.sale import Sale
from app.models.user import User
from app.models.vehicle import FuelType, TransmissionType, Vehicle, VehicleCondition
from app.repositories.sale_repository import SaleRepository


def create_test_session() -> Session:
    """Return an isolated in-memory database session."""
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def build_sale(vin: str, email: str) -> Sale:
    """Build a valid sale for repository tests."""
    return Sale(
        vehicle=Vehicle(
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
        ),
        seller=User(
            full_name="Ada Lovelace",
            email=email,
            hashed_password="hashed-value",
        ),
        customer_name="Grace Hopper",
        customer_email="grace@example.com",
        customer_phone="+15551234567",
        sale_price=Decimal("22000.00"),
        sale_date=datetime(2026, 7, 19, tzinfo=timezone.utc),
    )


def test_sale_repository_operations_are_transaction_scoped() -> None:
    session = create_test_session()
    repository = SaleRepository(session)
    first_sale = repository.create(build_sale("1HGCM82633A004352", "ada@example.com"))
    second_sale = repository.create(build_sale("1HGCM82633A004353", "alan@example.com"))

    assert repository.get_by_id(first_sale.id) is first_sale
    assert repository.get_by_vehicle_id(first_sale.vehicle_id) is first_sale
    assert repository.get_all() == [first_sale, second_sale]

    first_sale.customer_name = "Rear Admiral Grace Hopper"
    assert repository.update(first_sale).customer_name == "Rear Admiral Grace Hopper"

    repository.delete(second_sale)
    assert repository.get_by_id(second_sale.id) is None
    session.rollback()
    assert repository.get_by_id(first_sale.id) is None
    session.close()
