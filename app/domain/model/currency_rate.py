from dataclasses import dataclass


# INFO: I use dataclass to avoid __init__ declaraion
@dataclass
class CurrencyRate:
    currency: str
    rate: float
