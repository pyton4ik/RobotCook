"""
TODO
"""
from sqlalchemy.orm import Session

from models import Order, OrderItems, Product, Receipt
from chef import Recipe


def get_products_list(db: Session):
    return db.query(Product).filter(Product.active == True).all()


def create_product_order(db: Session, items):
    db_order = Order(name="test_order")
    db.add(db_order)
    db.commit()

    for item in items:
        product_obj = db.query(Product).filter(Product.id == item[0]).first()
        db_order_item = OrderItems(order_id=db_order.id,
                                   product_id=item[0],
                                   qty=item[1],
                                   price=product_obj.price)
        db.add(db_order_item)

    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_obj(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def cook_product_order(db: Session, order_id: int):
    order_obj = get_order_obj(db, order_id)
    for order_item in order_obj.order_items:
        receipt_objs = db.query(Receipt).filter(Receipt.product_id == order_item.product_id).all()
        receipt = [(recipe_item.ingredient,
                    recipe_item.operation,
                    recipe_item.wait_time) for recipe_item in receipt_objs]
        if order_item.remaining_qty > 0:
            for _ in range(order_item.remaining_qty):
                if create_from_raw_recipe(receipt):
                    order_item.processed_qty += 1
                    db.commit()

    return order_obj


def create_from_raw_recipe(items):
    return Recipe(items)
