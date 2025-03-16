"""add username, role fields for User model

Revision ID: 2ce450edccd0
Revises: 7c446b13278c
Create Date: 2025-03-15 21:24:24.960065

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2ce450edccd0"
down_revision: Union[str, None] = "7c446b13278c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
    """
    CREATE TYPE roleenum AS ENUM ('ADMIN', 'MANAGER', 'CUSTOMER');
    """
    )
    op.add_column("users", sa.Column("username", sa.String(), nullable=False))
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.Enum("ADMIN", "MANAGER", "CUSTOMER", name="roleenum"),
            server_default="CUSTOMER",
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "role")
    op.drop_column("users", "username")
    op.execute("DROP TYPE roleenum")
