"""create Order, OrderItem models

Revision ID: 0bd919c7673c
Revises: 4cb060e32d05
Create Date: 2025-03-24 00:24:16.554748

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


revision: str = "0bd919c7673c"
down_revision: Union[str, None] = "4cb060e32d05"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("user_id", sa.Integer(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_orders_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
    )
    op.create_index(
        op.f("ix_orders_created_at"), "orders", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_orders_updated_at"), "orders", ["updated_at"], unique=False
    )
    op.create_index(op.f("ix_orders_user_id"), "orders", ["user_id"], unique=False)
    op.create_table(
        "order_items",
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
            name=op.f("fk_order_items_order_id_orders"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_order_items_product_id_products"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("order_id", "product_id", name=op.f("pk_order_items")),
    )
    op.create_index(
        op.f("ix_order_items_created_at"),
        "order_items",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_order_items_order_id"),
        "order_items",
        ["order_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_order_items_product_id"),
        "order_items",
        ["product_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_order_items_updated_at"),
        "order_items",
        ["updated_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_order_items_updated_at"), table_name="order_items")
    op.drop_index(op.f("ix_order_items_product_id"), table_name="order_items")
    op.drop_index(op.f("ix_order_items_order_id"), table_name="order_items")
    op.drop_index(op.f("ix_order_items_created_at"), table_name="order_items")
    op.drop_table("order_items")
    op.drop_index(op.f("ix_orders_user_id"), table_name="orders")
    op.drop_index(op.f("ix_orders_updated_at"), table_name="orders")
    op.drop_index(op.f("ix_orders_created_at"), table_name="orders")
    op.drop_table("orders")
