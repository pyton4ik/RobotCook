"""
Pydantic schemas for FastAPI and Flask return values (convert SQLAlchemy models to JSON).
"""
from typing import List, Optional, Union
from typing_extensions import Literal
from pydantic import BaseModel, PositiveInt


class Product(BaseModel):
    id: int
    name: str
    type: str
    price: float

    class Config:
        orm_mode = True


class CreateOrderItem(BaseModel):
    product_id: int
    qty: int

    class Config:
        orm_mode = True


class CreateOrder(BaseModel):
    name: str
    ref: Optional[str]
    order_items: List[CreateOrderItem] = []


class ReadOrderItem(CreateOrderItem):
    id: int
    processed_qty: int
    remaining_qty: int
    price: float
    total: float

    class Config:
        orm_mode = True


class ReadOrder(BaseModel):
    id: int
    name: str
    ref: str
    state: str
    total: float
    total_payment: float
    is_paid: bool
    is_done: bool
    order_items: List[ReadOrderItem]

    class Config:
        orm_mode = True


class RawOrderItem(BaseModel):
    ingredient: str
    operation: Union[str, Literal[""], None]
    time: Union[PositiveInt, Literal[""], None]


class RawOrder(BaseModel):
    items: List[RawOrderItem] = []
