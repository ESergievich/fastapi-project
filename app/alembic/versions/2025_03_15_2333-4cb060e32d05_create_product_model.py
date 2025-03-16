"""create Product model

Revision ID: 4cb060e32d05
Revises: 2ce450edccd0
Create Date: 2025-03-15 23:33:25.933947

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


revision: str = "4cb060e32d05"
down_revision: Union[str, None] = "2ce450edccd0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
    )
    op.create_index(
        op.f("ix_products_created_at"),
        "products",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_products_name"), "products", ["name"], unique=True
    )
    op.create_index(
        op.f("ix_products_slug"), "products", ["slug"], unique=True
    )
    op.create_index(
        op.f("ix_products_updated_at"),
        "products",
        ["updated_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_products_updated_at"), table_name="products")
    op.drop_index(op.f("ix_products_slug"), table_name="products")
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_index(op.f("ix_products_created_at"), table_name="products")
    op.drop_table("products")
