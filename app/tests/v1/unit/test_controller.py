"""
Controller Adapter methods for control cooking.
"""
from app.v1.controller import cook_product_order
from app.v1.controller import create_from_raw_recipe
from app.v1.controller import create_product_order
from app.v1.controller import get_products_list


def test_get_products_list(db_init_products, database):
    res = get_products_list(database)
    assert len(res) == 3
    assert res[0].name == "test_sale_product0"
    assert res[0].type == "sale"
    assert res[0].active is True
    assert res[0].price > 0.01
    assert len(res[0].receipts) > 0


def test_create_product_order(database, db_init_products):
    for product in db_init_products:
        assert len(product.order_items) == 0

    order = create_product_order(
        database,
        order_items=[
            {"product_id": db_init_products[0].id, "qty": 1},
            {"product_id": db_init_products[1].id, "qty": 2},
            {"product_id": db_init_products[2].id, "qty": 3},
        ],
    )

    for product in db_init_products:
        assert len(product.order_items) > 0

    assert len(order.order_items) == 3
    assert sum(item.remaining_qty for item in order.order_items) > 0


def test_cook_product_order(database, db_init_products):
    order_obj = cook_product_order(database, 1)
    assert sum(item.remaining_qty for item in order_obj.order_items) == 0


async def test_create_from_raw_recipe(database, raw_recipe_hot_dog):
    await create_from_raw_recipe(raw_recipe_hot_dog)
