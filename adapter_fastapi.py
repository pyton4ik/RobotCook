"""
Scheamas module
"""
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods

from typing import List, Optional, Union
from typing_extensions import Literal
from pydantic import BaseModel, PositiveInt
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from database import SessionLocal, engine
import models
import controller


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


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products/", response_model=list[Product])
def read_products(db: Session = Depends(get_db)):
    users = controller.get_products_list(db)
    return users


@app.post("/order/", response_model=ReadOrder)
def create_order(datas: CreateOrder, db: Session = Depends(get_db)):
    ret_val = controller.create_product_order(db, **dict(datas))
    return ret_val


@app.get("/order/cook/{order_id}", response_model=ReadOrder)
def cook_order(order_id: int, db: Session = Depends(get_db)):
    db_order = controller.cook_product_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.get("/order/{order_id}", response_model=ReadOrder)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = controller.get_order_obj(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.post("/raw_recipe/")
def create_raw_recipe(datas: RawOrder):
    return controller.create_from_raw_recipe(datas.items)
