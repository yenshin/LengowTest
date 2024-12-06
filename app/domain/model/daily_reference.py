from dataclasses import dataclass
from datetime import date
from typing import Dict

from app.domain.model.currency_rate import CurrencyRate


# INFO: I use dataclass to avoid __init__ declaraion
@dataclass
class DailyReference:
    date: date
    currencies: Dict[str, CurrencyRate]
