"""Create the purchase table.

Revision ID: 20260719_03
Revises: 20260719_02
Create Date: 2026-07-19 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260719_03"
down_revision: Union[str, None] = "20260719_02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


purchase_payment_status = postgresql.ENUM(
    "PENDING",
    "PAID",
    name="purchase_payment_status",
    create_type=False,
)


def upgrade() -> None:
    """Create the vehicle-acquisition table and its payment-status enum."""
    bind = op.get_bind()
    purchase_payment_status.create(bind, checkfirst=True)
    op.create_table(
        "purchase",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("vehicle_id", sa.Integer(), nullable=False),
        sa.Column("supplier_name", sa.String(length=255), nullable=False),
        sa.Column("purchase_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("purchase_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("invoice_number", sa.String(length=100), nullable=False),
        sa.Column(
            "payment_status",
            purchase_payment_status,
            nullable=False,
            server_default=sa.text("'PENDING'"),
        ),
        sa.Column("notes", sa.Text(), nullable=True),
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
        sa.CheckConstraint(
            "purchase_price > 0",
            name="ck_purchase_purchase_price_positive",
        ),
        sa.ForeignKeyConstraint(
            ["vehicle_id"],
            ["vehicle.id"],
            name="fk_purchase_vehicle_id_vehicle",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("vehicle_id", name="uq_purchase_vehicle_id"),
        sa.UniqueConstraint("invoice_number", name="uq_purchase_invoice_number"),
    )


def downgrade() -> None:
    """Drop the vehicle-acquisition table and its payment-status enum."""
    op.drop_table("purchase")
    purchase_payment_status.drop(op.get_bind(), checkfirst=True)
