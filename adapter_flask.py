"""
Test for Flask adapter
"""
from typing import List

from flask import Flask
from flask import request
from flask import jsonify, abort
from pydantic import parse_obj_as

import controller
from database import SessionLocal
from schemas import Product, ReadOrder

app = Flask(__name__)


@app.route("/products/", methods=["GET"])
def read_products():
    parsed_objs = parse_obj_as(List[Product], controller.get_products_list(SessionLocal()))
    return jsonify([item.dict() for item in parsed_objs])


@app.route("/order/", methods=["POST"])
def create_order():
    request_data = request.get_json()
    res = controller.create_product_order(SessionLocal(), **dict(request_data))
    return jsonify(ReadOrder.from_orm(res).dict())


@app.route("/order/", methods=["GET"])
def read_order():
    order_id = request.args.get("order_id")
    res = controller.get_order_obj(SessionLocal(), order_id)
    if not res:
        abort(404, description="Order not found")
    return jsonify(ReadOrder.from_orm(res).dict())


@app.route("/order/cook/", methods=["GET"])
def cook_product_order():
    order_id = request.args.get("order_id")
    res = controller.get_order_obj(SessionLocal(), order_id)
    if not res:
        abort(404, description="Order not found")
    return jsonify(ReadOrder.from_orm(res).dict())


@app.route("/raw_recipe/", methods=["POST"])
def create_raw_recipe():
    request_data = request.get_json()
    controller.create_from_raw_recipe(request_data["items"])
    return jsonify(success=True)
