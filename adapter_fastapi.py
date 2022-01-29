"""
Scheamas module
"""
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from database import SessionLocal, engine
import models
import controller
import schemas
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products/", response_model=list[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    return controller.get_products_list(db)


@app.post("/order/", response_model=schemas.ReadOrder)
def create_order(datas: schemas.CreateOrder, db: Session = Depends(get_db)):
    ret_val = controller.create_product_order(db, **dict(datas))
    return ret_val


@app.get("/order/cook/{order_id}", response_model=schemas.ReadOrder)
def cook_order(order_id: int, db: Session = Depends(get_db)):
    db_order = controller.cook_product_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.get("/order/{order_id}", response_model=schemas.ReadOrder)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = controller.get_order_obj(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.post("/raw_recipe/")
def create_raw_recipe(datas: schemas.RawOrder):
    return controller.create_from_raw_recipe(datas.items)
