"""Create the vehicle table.

Revision ID: 20260719_02
Revises: 20260719_01
Create Date: 2026-07-19 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260719_02"
down_revision: Union[str, None] = "20260719_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


fuel_type = postgresql.ENUM(
    "PETROL",
    "DIESEL",
    "CNG",
    "ELECTRIC",
    "HYBRID",
    name="fuel_type",
    create_type=False,
)
transmission_type = postgresql.ENUM(
    "MANUAL",
    "AUTOMATIC",
    name="transmission_type",
    create_type=False,
)
vehicle_condition = postgresql.ENUM(
    "NEW",
    "USED",
    name="vehicle_condition",
    create_type=False,
)
vehicle_status = postgresql.ENUM(
    "AVAILABLE",
    "SOLD",
    name="vehicle_status",
    create_type=False,
)


def upgrade() -> None:
    """Create the vehicle table and its supporting enums and index."""
    bind = op.get_bind()
    fuel_type.create(bind, checkfirst=True)
    transmission_type.create(bind, checkfirst=True)
    vehicle_condition.create(bind, checkfirst=True)
    vehicle_status.create(bind, checkfirst=True)
    op.create_table(
        "vehicle",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("manufacturer", sa.String(length=50), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=False),
        sa.Column("vin", sa.String(length=17), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("purchase_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("selling_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("color", sa.String(length=30), nullable=False),
        sa.Column("mileage", sa.Integer(), nullable=False),
        sa.Column("fuel_type", fuel_type, nullable=False),
        sa.Column("transmission", transmission_type, nullable=False),
        sa.Column("condition", vehicle_condition, nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            vehicle_status,
            nullable=False,
            server_default=sa.text("'AVAILABLE'"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint("mileage >= 0", name="ck_vehicle_mileage_non_negative"),
        sa.CheckConstraint(
            "purchase_price > 0",
            name="ck_vehicle_purchase_price_positive",
        ),
        sa.CheckConstraint(
            "selling_price > 0",
            name="ck_vehicle_selling_price_positive",
        ),
        sa.UniqueConstraint("vin", name="uq_vehicle_vin"),
    )
    op.create_index("idx_vehicle_status", "vehicle", ["status"], unique=False)


def downgrade() -> None:
    """Drop the vehicle table and its supporting enums and index."""
    op.drop_index("idx_vehicle_status", table_name="vehicle")
    op.drop_table("vehicle")
    bind = op.get_bind()
    vehicle_status.drop(bind, checkfirst=True)
    vehicle_condition.drop(bind, checkfirst=True)
    transmission_type.drop(bind, checkfirst=True)
    fuel_type.drop(bind, checkfirst=True)
