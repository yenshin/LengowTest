"""split conversion model in something more durable for data science

Revision ID: a1a992e78b34
Revises: 77848694d299
Create Date: 2024-12-09 10:32:23.778993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1a992e78b34'
down_revision: Union[str, None] = '77848694d299'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
