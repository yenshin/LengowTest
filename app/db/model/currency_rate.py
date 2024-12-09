import uuid as uid

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from app.db.model.basemodel import BaseModel
from app.db.model.daily_reference import DailyReference


class CurrencyRate(BaseModel):
    __tablename__ = "currencyrate"
    dailyref_id: Mapped[uid.UUID] = mapped_column(
        postgresql.UUID,
        sa.ForeignKey(DailyReference.id, ondelete="CASCADE"),
        primary_key=True,
        index=True,
        nullable=False,
    )
    currency_type: Mapped[str] = mapped_column(sa.String, index=True, nullable=False)
    currency_rate: Mapped[float] = mapped_column(sa.Float, nullable=False)
