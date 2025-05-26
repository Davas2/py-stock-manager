from datetime import datetime
from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    quantity: int
    unit_price: float
    created_at: datetime

@dataclass
class User:
    id: int
    name: str
    email: str

@dataclass
class Movement:
    id: int
    user_id: int
    product_id: int
    quantity: int
    unit_price: float
    created_at: datetime
    