"""create current table

Revision ID: 77848694d299
Revises:
Create Date: 2024-12-09 09:44:10.887892

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "77848694d299"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dailyreference",
        sa.Column("id", sa.UUID, primary_key=True, nullable=False),
        sa.Column("date", sa.DATE, nullable=False),
        sa.Column("currencies", sa.JSON),
    )
    op.create_index(
        op.f("idx_dailyreference_date"), "dailyreference", ["date"], unique=False
    )


def downgrade() -> None:
    op.drop_table("dailyreference")
