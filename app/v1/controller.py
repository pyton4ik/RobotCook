"""
TODO
"""
from sqlalchemy.orm import Session

from app.v1.chef import Recipe
from app.v1.errors import ProductNotFound
from app.v1.models import Order
from app.v1.models import OrderItems
from app.v1.models import Product
from app.v1.models import Receipt


def get_product(db: Session, product_id):
    res = db.query(Product).filter(Product.id == product_id).first()
    if res is None:
        raise ProductNotFound(product=product_id)
    return res


def get_products_list(db: Session):
    return db.query(Product).filter(Product.active == True).all()


def create_product_order(db: Session, **kwargs):
    """Create product order in DB but not cooking it"""

    curr_kwargs = kwargs.copy()
    items = curr_kwargs.pop("order_items")
    db_order = Order(**curr_kwargs)
    db.add(db_order)
    db.commit()

    for item in items:
        item = dict(item)
        product_obj = (
            db.query(Product).filter(Product.id == item.get("product_id")).first()
        )
        db_order_item = OrderItems(
            order_id=db_order.id,
            product_id=product_obj.id,
            qty=item.get("qty"),
            price=product_obj.price,
        )
        db.add(db_order_item)
        db.commit()

    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_obj(db: Session, order_id: int):
    """
    :param db: Alchemy Session
    :param order_id: order ID
    :return: Alchemy Order object
    """
    return db.query(Order).filter(Order.id == order_id).first()


def get_receipt_item(db: Session, product_id: int):
    """

    :param db: Alchemy Session
    :param product_id: Product ID
    :return: Receip Array dict with keys (ingredient, operation, time)
    """
    receipt_objs = db.query(Receipt).filter(Receipt.product_id == product_id).all()
    return [
        {
            "ingredient": recipe_item.ingredient,
            "operation": recipe_item.operation,
            "time": recipe_item.wait_time,
        }
        for recipe_item in receipt_objs
    ]


def cook_product_order(db: Session, order_id: int):
    order_obj = get_order_obj(db, order_id)
    for order_item in order_obj.order_items:
        receipt = get_receipt_item(db, order_item.product_id)
        if order_item.remaining_qty > 0:
            for _ in range(order_item.remaining_qty):
                if create_from_raw_recipe(receipt):
                    order_item.processed_qty += 1
                    db.commit()

    order_obj.state = "ready"
    db.commit()
    return order_obj


async def cook_product_id(db: Session, product_id: int, node=""):
    receipt = get_receipt_item(db, product_id)
    await create_from_raw_recipe(receipt)
    print(f"The node {node} has finished cooking the product {product_id}")


async def create_from_raw_recipe(items):
    return await Recipe(items)()
