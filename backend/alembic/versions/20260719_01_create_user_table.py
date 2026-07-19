"""Create the user table.

Revision ID: 20260719_01
Revises:
Create Date: 2026-07-19 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260719_01"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_role = postgresql.ENUM(
    "ADMIN",
    "EMPLOYEE",
    name="user_role",
    create_type=False,
)


def upgrade() -> None:
    """Create the user table and its supporting enum and index."""
    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default=sa.text("'EMPLOYEE'"),
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
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
    )
    op.create_index(op.f("idx_user_email"), "user", ["email"], unique=True)


def downgrade() -> None:
    """Drop the user table and supporting enum."""
    op.drop_index(op.f("idx_user_email"), table_name="user")
    op.drop_table("user")
    user_role.drop(op.get_bind(), checkfirst=True)
