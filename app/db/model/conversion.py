import json
from typing import Dict

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db.model.basemodel import BaseModel
from app.domain.model.currency_rate import CurrencyRate
from app.domain.model.daily_reference import DailyReference as dr_dom


class DailyReference(BaseModel):
    __tablename__ = "dailyreference"
    date: Mapped[sa.Date] = mapped_column(
        sa.Date,
        index=True,
        nullable=False,
    )
    # INFO: we could do a clerver storage for smart manipulation
    # exemple: evolution of currency bla bla
    # by making 2 table but my time is limited
    # for the moment I will keep it like this
    currencies: Mapped[sa.JSON] = mapped_column(sa.JSON, index=False, nullable=False)

    # INFO: I'm out of time to do something clean
    # utility function to simplify manipulation
    def GetDomainModel(self):
        jsonparsed_curr = json.loads(self.currencies)
        concerted_currencies: Dict[str, CurrencyRate] = {}
        for key in jsonparsed_curr:
            val = jsonparsed_curr[key]
            concerted_currencies[key] = CurrencyRate(
                currency=val["currency"],
                rate=val["rate"],
            )
        return dr_dom(date=self.date, currencies=concerted_currencies)
