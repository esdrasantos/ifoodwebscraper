from dataclasses import dataclass
from typing import List

@dataclass
class Item:
    name: str
    price: float
    quantity: int
    obs : str

@dataclass
class Order:
    id: str
    restaurant: str
    total: float
    items: List[Item] = None
