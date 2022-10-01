"""
Test for Flask adapter
"""
from typing import List

from flask import abort
from flask import Flask
from flask import jsonify
from flask import request
from pydantic import parse_obj_as

from app.v1 import controller
from app.v1.database import SessionLocal
from app.v1.schemas import Product
from app.v1.schemas import ReadOrder

app = Flask(__name__)
session = SessionLocal()


@app.route("/products/", methods=["GET"])
def read_products():
    parsed_objs = parse_obj_as(List[Product], controller.get_products_list(session))
    return jsonify([item.dict() for item in parsed_objs])


@app.route("/order/", methods=["POST"])
def create_order():
    request_data = request.get_json()
    res = controller.create_product_order(session, **dict(request_data))
    return jsonify(ReadOrder.from_orm(res).dict())


@app.route("/order/", methods=["GET"])
def read_order():
    order_id = request.args.get("order_id")
    res = controller.get_order_obj(session, order_id)
    if not res:
        abort(404, description="Order not found")
    return jsonify(ReadOrder.from_orm(res).dict())


@app.route("/order/cook/", methods=["GET"])
def cook_product_order():
    order_id = request.args.get("order_id")
    res = controller.get_order_obj(session, order_id)
    if not res:
        abort(404, description="Order not found")
    return jsonify(ReadOrder.from_orm(res).dict())


@app.route("/raw_recipe/", methods=["POST"])
async def create_raw_recipe():
    request_data = request.get_json()
    await controller.create_from_raw_recipe(request_data["items"])
    return jsonify(success=True)
