"""split conversion model in something more durable for data science

Revision ID: a1a992e78b34
Revises: 77848694d299
Create Date: 2024-12-09 10:32:23.778993

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1a992e78b34"
down_revision: Union[str, None] = "77848694d299"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "currencyrate",
        sa.Column("id", sa.UUID, primary_key=True, nullable=False),
        sa.Column("dailyref_id", sa.UUID, nullable=False),
        sa.Column("currency_type", sa.String, nullable=False),
        sa.Column("currency_rate", sa.REAL, nullable=False),
        sa.ForeignKeyConstraint(
            ["dailyref_id"], ["dailyreference.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("idx_currencyrate_dailyref_id"),
        "currencyrate",
        ["dailyref_id"],
        unique=False,
    )
    op.create_index(
        op.f("idx_currencyrate_currency_type"),
        "currencyrate",
        ["currency_type"],
        unique=False,
    )
    # INFO: drop the json because we are ate an early stage
    # in other circumstence we need to do a db migration
    with op.batch_alter_table("dailyreference") as batch_op:
        batch_op.drop_column("currencies")


def downgrade() -> None:
    op.drop_index(op.f("idx_currencyrate_dailyref_id"), table_name="employee")
    op.drop_index(op.f("idx_currencyrate_currency_type"), table_name="employee")
    op.drop_table("currencyrate")
