from dataclasses import dataclass


# INFO: I use dataclass to avoid __init__ declaraion
@dataclass
class ConversionModel:
    __modelname__ = "conversion"
    currency: str
    rate: float
