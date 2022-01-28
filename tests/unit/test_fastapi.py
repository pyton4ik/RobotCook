# pylint: disable=missing-function-docstring
import mock
import pytest

from fastapi.testclient import TestClient
from adapter_fastapi import app


@pytest.fixture
def fastapi_client(path_mock_delay):
    return TestClient(app)


@pytest.fixture
def product_order_dict():
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


def test_get_products_list(monkeypatch, db_init_products, fastapi_client):
    response = fastapi_client.get("/products/")
    assert response.status_code == 200
    res_json = response.json()

    assert len(res_json) == 3
    assert res_json[0] == {
        "id": 1,
        "name": "test_sale_product0",
        "price": 99.98,
        "type": "sale"
    }


def test_create_product_order(monkeypatch, db_init_products, fastapi_client, product_order_dict):
    order_items = [{"product_id": product.id, "qty": product.id} for product in db_init_products]
    response = fastapi_client.post("/order/", json={"name": "fastapi_test_order",
                                                    "ref": "555",
                                                    "order_items": order_items})
    assert response.status_code == 200
    res_json = response.json()
    assert res_json == product_order_dict
    assert len(res_json["order_items"]) == len(order_items)
    for index, item in enumerate(res_json["order_items"]):
        assert item["product_id"] == index + 1
        assert item["qty"] == index + 1


@pytest.mark.parametrize("route", ["/order/cook/2", "/order/2"])
def test_cook_order(monkeypatch, fastapi_client, product_order_dict, route):
    order_id = 2
    response = fastapi_client.get(route)
    assert response.status_code == 200
    res_json = response.json()
    product_order_dict["is_done"] = True
    assert res_json == product_order_dict


def test_raw_recipe(monkeypatch, fastapi_client, raw_recipe_hot_dog):
    response = fastapi_client.post("/raw_recipe/", json={"items": raw_recipe_hot_dog})
    assert response.status_code == 200
    res_json = response.json()
