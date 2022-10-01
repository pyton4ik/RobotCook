from typing import List

from aiohttp import web
from pydantic import parse_obj_as

from app.v1 import controller
from app.v1.database import SessionLocal
from app.v1.schemas import Product
from app.v1.schemas import ReadOrder

session = SessionLocal()


async def read_products(request):
    parsed_objs = parse_obj_as(List[Product], controller.get_products_list(session))
    data = [item.dict() for item in parsed_objs]
    return web.json_response(data)


async def create_order(request):
    request_data = await request.post()
    res = controller.create_product_order(session, **dict(request_data))
    return web.json_response(ReadOrder.from_orm(res).dict())


async def read_order(request):
    order_id = request.args.get("order_id")
    res = controller.get_order_obj(session, order_id)
    if not res:
        raise web.HTTPFound
    return web.json_response(ReadOrder.from_orm(res).dict())


async def cook_product_order(request):
    order_id = request.args.get("order_id")
    res = controller.get_order_obj(session, order_id)
    if not res:
        raise web.HTTPFound
    return web.json_response(ReadOrder.from_orm(res).dict())


async def create_raw_recipe(request):
    request_data = request.get_json()
    await controller.create_from_raw_recipe(request_data["items"])
    return web.json_response(success=True)


ROUTERS = [
    web.get("/products/", read_products),
    web.post("/order/", create_order),
    web.get("/order/{order_id}", read_order),
    web.get("/order/cook/{order_id}", cook_product_order),
    web.post("/raw_recipe/", create_raw_recipe),
]

app = web.Application()
app.add_routes(ROUTERS)

if __name__ == "__main__":
    web.run_app(app)
