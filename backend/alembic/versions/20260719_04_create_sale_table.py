"""Create the sale table.

Revision ID: 20260719_04
Revises: 20260719_03
Create Date: 2026-07-19 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260719_04"
down_revision: Union[str, None] = "20260719_03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the completed-vehicle-sale table and its indexes."""
    op.create_table(
        "sale",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("vehicle_id", sa.Integer(), nullable=False),
        sa.Column("seller_id", sa.Integer(), nullable=False),
        sa.Column("customer_name", sa.String(length=255), nullable=False),
        sa.Column("customer_email", sa.String(length=255), nullable=False),
        sa.Column("customer_phone", sa.String(length=20), nullable=False),
        sa.Column("sale_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("sale_date", sa.DateTime(timezone=True), nullable=False),
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
        sa.CheckConstraint("sale_price > 0", name="ck_sale_sale_price_positive"),
        sa.ForeignKeyConstraint(
            ["vehicle_id"],
            ["vehicle.id"],
            name="fk_sale_vehicle_id_vehicle",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["seller_id"],
            ["user.id"],
            name="fk_sale_seller_id_user",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("vehicle_id", name="uq_sale_vehicle_id"),
    )
    op.create_index("idx_sale_seller_id", "sale", ["seller_id"], unique=False)


def downgrade() -> None:
    """Drop the completed-vehicle-sale table and its index."""
    op.drop_index("idx_sale_seller_id", table_name="sale")
    op.drop_table("sale")
