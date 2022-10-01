"""
Pytest with native aiohttp.test_utils.TestClient client
"""
import time

import pytest
from aiohttp import web

from app.v1.adapters.adapter_aiohttp import ROUTERS


@pytest.fixture
def aiohttp_client(loop, aiohttp_client):
    app = web.Application()
    app.add_routes(ROUTERS)
    return loop.run_until_complete(aiohttp_client(app))


async def test_get_products_list(aiohttp_client, product_dict):
    response = await aiohttp_client.get("/products/")
    assert response.status == 200
    res_json = await response.json()
    time.sleep(3)
    assert len(res_json) == 3
    assert res_json[0] == product_dict


async def test_create_product_order(
    monkeypatch, db_init_products, aiohttp_client, order_dict, db_init_products_dict
):
    response = await aiohttp_client.post(
        "/order/",
        json={
            "name": "aiohttp_test_order",
            "ref": "aiohttp_555",
            "order_items": db_init_products_dict,
        },
    )
    assert response.status == 200
    res_json = await response.json()
    assert res_json == order_dict
    assert len(res_json["order_items"]) == len(db_init_products_dict)
    for index, item in enumerate(res_json["order_items"]):
        assert item["product_id"] == index + 1
        assert item["qty"] == index + 1


@pytest.mark.parametrize("route", ["/order/cook/2", "/order/2"])
async def test_cook_order(aiohttp_client, order_dict, route):
    response = await aiohttp_client.get(route)
    assert response.status == 200
    res_json = await response.json()
    order_dict["is_done"] = True
    assert res_json == order_dict
