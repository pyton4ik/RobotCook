import pytest
import mock

from database import SessionLocal
import hardware
from models import Product, Receipt


@pytest.fixture
def path_mock_delay(monkeypatch):
    monkeypatch.setattr(hardware, "SOUCE_OPEN_WAIT_TIME", 0)


@pytest.fixture(scope="session")
def database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db_init_products(database):
    """
    :param database: Init DB section fixture
    :return: SQLAProduct objects list
    """
    ret_val = []
    for index_name in range(3):
        product_obj = Product(name="test_sale_product{}".format(index_name), price=99.98, type="sale")
        database.add(product_obj)
        database.commit()
        database.refresh(product_obj)

        database.add(Receipt(ingredient="box s", product_id=product_obj.id))
        database.add(Receipt(ingredient="fries", operation="fryer", wait_time=300, product_id=product_obj.id))

        ret_val.append(product_obj)

    database.commit()
    return ret_val


@pytest.fixture
def db_init_products_dict(db_init_products):
    return [{"product_id": product.id, "qty": product.id} for product in db_init_products]


@pytest.fixture
def raw_recipe_hot_dog(path_mock_delay):
    return [{"ingredient": "box m", "operation": None, "time": None},
            {"ingredient": "hot dog bun", "operation": None, "time": None},
            {"ingredient": "sausage", "operation": "grill", "time": 180},
            {"ingredient": "pickle", "operation": None, "time": None},
            {"ingredient": "tomato", "operation": None, "time": None},
            {"ingredient": "mustard", "operation": None, "time": None}]


@pytest.fixture
def product_dict():
    return {
        "id": 1,
        "name": "test_sale_product0",
        "price": 99.98,
        "type": "sale"
    }


@pytest.fixture
def order_dict():
    return {
        "id": mock.ANY,
        "name": "fastapi_test_order",
        "ref": "555",
        "state": "draft",
        "total": mock.ANY,
        "total_payment": 0.00,
        "is_paid": False,
        "is_done": False,
        "order_items": mock.ANY
    }
