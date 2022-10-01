from unittest import mock

import pytest

from app.v1.adapters.adapter_flask import app


@pytest.fixture
def flask_client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def flask_order_params(db_init_products_dict):
    return {
        "name": "flask_test_order",
        "ref": "Flask777",
        "order_items": db_init_products_dict,
    }


@pytest.fixture
def flask_order_info(order_dict, flask_order_params):
    order_dict.update(flask_order_params)
    order_dict["order_items"] = mock.ANY
    return order_dict


def test_get_products_list(flask_client, product_dict):
    response = flask_client.get("/products/")

    res_json = response.get_json()

    assert len(res_json) == 3
    assert res_json[0] == product_dict


def test_create_order(flask_client, flask_order_info, flask_order_params):
    response = flask_client.post("/order/", json=flask_order_params)
    assert response.status_code == 200

    res_json = response.get_json()
    assert res_json == flask_order_info


def test_read_order(flask_client, flask_order_info, db_init_products_dict):
    order_id = 3
    response = flask_client.get("/order/", query_string={"order_id": order_id})
    assert response.status_code == 200
    res_json = response.get_json()

    assert res_json == flask_order_info
    assert len(res_json["order_items"]) == len(db_init_products_dict)
    for index, item in enumerate(res_json["order_items"]):
        assert item["product_id"] == index + 1
        assert item["qty"] == index + 1


def test_read_not_exist_order(flask_client, flask_order_info, db_init_products_dict):
    order_id = 555
    response = flask_client.get("/order/", query_string={"order_id": order_id})
    assert response.status_code == 404


def test_create_raw_recipe(flask_client, raw_recipe_hot_dog):
    response = flask_client.post("/raw_recipe/", json={"items": raw_recipe_hot_dog})
    assert response.status_code == 200
