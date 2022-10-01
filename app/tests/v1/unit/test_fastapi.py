import pytest
from fastapi.testclient import TestClient

from app.v1.adapters.adapter_fastapi import app


@pytest.fixture
def fastapi_client(path_mock_delay):
    return TestClient(app)


def test_get_products_list(monkeypatch, db_init_products, fastapi_client, product_dict):
    response = fastapi_client.get("/products/")
    assert response.status_code == 200
    res_json = response.json()

    assert len(res_json) == 3
    assert res_json[0] == product_dict


def test_create_product_order(
    monkeypatch, db_init_products, fastapi_client, order_dict, db_init_products_dict
):
    response = fastapi_client.post(
        "/order/",
        json={
            "name": "fastapi_test_order",
            "ref": "555",
            "order_items": db_init_products_dict,
        },
    )
    assert response.status_code == 200
    res_json = response.json()
    assert res_json == order_dict
    assert len(res_json["order_items"]) == len(db_init_products_dict)
    for index, item in enumerate(res_json["order_items"]):
        assert item["product_id"] == index + 1
        assert item["qty"] == index + 1


@pytest.mark.parametrize("route", ["/order/cook/2", "/order/2"])
def test_cook_order(monkeypatch, fastapi_client, order_dict, route):
    response = fastapi_client.get(route)
    assert response.status_code == 200
    res_json = response.json()
    order_dict["is_done"] = True
    assert res_json == order_dict


def test_raw_recipe(monkeypatch, fastapi_client, raw_recipe_hot_dog):
    response = fastapi_client.post("/raw_recipe/", json={"items": raw_recipe_hot_dog})
    assert response.status_code == 200
