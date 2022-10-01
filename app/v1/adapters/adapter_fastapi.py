"""
Scheamas module
"""
import controller
import models
import schemas
from database import engine
from database import SessionLocal
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

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
    return controller.create_product_order(db, **dict(datas))


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
async def create_raw_recipe(datas: schemas.RawOrder):
    await controller.create_from_raw_recipe(datas.items)
