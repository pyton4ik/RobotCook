"""
Scheamas module
"""
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from database import SessionLocal, engine
import models
import controller
from . import schemas


class Product(BaseModel):
    id: int

    class Config:
        orm_mode = True


class ProductOrderItem(BaseModel):
    product_id: Product
    qty: int


class ProductOrder(BaseModel):
    items: List[ProductOrderItem] = []


class RawOrderItem(BaseModel):
    product_name: str
    qty: int


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


@app.get("/order/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = controller.get_order_obj(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.post("/order/", response_model=schemas.ProductOrder)
def create_order(items: list[schemas.ProductOrder], db: Session = Depends(get_db)):
    return controller.create_product_order(db, items=items)


@app.get("/products/", response_model=list[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    users = controller.get_products_list(db)
    return users


@app.post("/raw_recipe/")
def create_raw_recipe(items: list[schemas.ProductOrder], db: Session = Depends(get_db)):
    return controller.create_from_raw_recipe(db, items)
