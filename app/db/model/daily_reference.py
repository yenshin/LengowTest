
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db.model.basemodel import BaseModel


class DailyReference(BaseModel):
    __tablename__ = "dailyreference"
    # INFO: I do not set unique = true for this test because we want
    # to test things, normally I would add it
    date: Mapped[sa.Date] = mapped_column(
        sa.Date,
        index=True,
        nullable=False,
    )
