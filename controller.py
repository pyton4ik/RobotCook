"""
TODO
"""
from sqlalchemy.orm import Session

from models import Order, OrderItems, Product, Receipt
from chef import Recipe


def get_products_list(db: Session):
    return db.query(Product).filter(Product.active == True).all()


def create_product_order(db: Session, **kwargs):

    curr_kwargs = kwargs.copy()
    items = curr_kwargs.pop("order_items")
    db_order = Order(**curr_kwargs)
    db.add(db_order)
    db.commit()

    for item in items:
        item = dict(item)
        product_obj = db.query(Product).filter(Product.id == item.get("product_id")).first()
        db_order_item = OrderItems(order_id=db_order.id,
                                   product_id=product_obj.id,
                                   qty=item.get("qty"),
                                   price=product_obj.price)
        db.add(db_order_item)
        db.commit()

    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_obj(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def cook_product_order(db: Session, order_id: int):
    order_obj = get_order_obj(db, order_id)
    for order_item in order_obj.order_items:
        receipt_objs = db.query(Receipt).filter(Receipt.product_id == order_item.product_id).all()
        receipt = [{"ingredient": recipe_item.ingredient,
                    "operation": recipe_item.operation,
                    "time": recipe_item.wait_time} for recipe_item in receipt_objs]
        if order_item.remaining_qty > 0:
            for _ in range(order_item.remaining_qty):
                if create_from_raw_recipe(receipt):
                    order_item.processed_qty += 1
                    db.commit()

    return order_obj


def create_from_raw_recipe(items):
    return Recipe(items)
