import json
import threading

import pika
import pytest

from app.v1.adapters import adapter_rabbitmq

CONNECTION_HOST = "localhost"


@pytest.fixture(scope="session", autouse=True)
def consume():
    def _forever():
        adapter_rabbitmq.channel.start_consuming()

    thd = threading.Thread(target=_forever)
    thd.daemon = True
    thd.start()


@pytest.fixture(scope="session")
def channel(consume):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(adapter_rabbitmq.CONNECTION_HOST)
    )
    channel = connection.channel()
    channel.queue_purge(queue=adapter_rabbitmq.QUEUE_CREATE_ORDER)
    channel.queue_purge(queue=adapter_rabbitmq.QUEUE_COOK)
    channel.queue_purge(queue=adapter_rabbitmq.QUEUE_RAW_RECIPE)
    return channel


def test_create_order(channel, db_init_products_dict):
    datas = {
        "name": "rabbitmq_test_order",
        "ref": "7778",
        "order_items": db_init_products_dict,
    }
    channel.basic_publish(
        exchange="",
        routing_key=adapter_rabbitmq.QUEUE_CREATE_ORDER,
        body=json.dumps(datas),
    )


def test_cook_order(channel):
    order_id = 4
    channel.basic_publish(
        exchange="", routing_key=adapter_rabbitmq.QUEUE_COOK, body=str(order_id)
    )


def test_raw_recipe(channel, raw_recipe_hot_dog):
    datas = {"items": raw_recipe_hot_dog}
    channel.basic_publish(
        exchange="",
        routing_key=adapter_rabbitmq.QUEUE_RAW_RECIPE,
        body=json.dumps(datas),
    )
