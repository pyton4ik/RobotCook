"""
RabbitMq layer adapter
"""
import json

import controller
import pika
from database import SessionLocal

CONNECTION_HOST = "localhost"

connection = pika.BlockingConnection(pika.ConnectionParameters(CONNECTION_HOST))
channel = connection.channel()

session = SessionLocal()

QUEUE_CREATE_ORDER = "create_order"
QUEUE_COOK = "cook_order"
QUEUE_RAW_RECIPE = "raw_recipe"


def create_order(channel, method, properties, body):
    datas = json.loads(body.decode("utf-8"))
    controller.create_product_order(session, **dict(datas))
    channel.basic_ack(delivery_tag=method.delivery_tag)


def cook_order(channel, method, properties, body):
    order_id = int(body)
    db_order = controller.cook_product_order(session, order_id=order_id)
    if db_order is None:
        channel.basic_ack(delivery_tag=method.delivery_tag)
    return db_order


def create_raw_recipe(channel, method, properties, body):
    datas = json.loads(body)
    controller.create_from_raw_recipe(datas.items)
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.queue_declare(queue=QUEUE_CREATE_ORDER)
channel.queue_declare(queue=QUEUE_COOK)
channel.queue_declare(queue=QUEUE_RAW_RECIPE)

channel.basic_consume(on_message_callback=create_order, queue=QUEUE_CREATE_ORDER)
channel.basic_consume(on_message_callback=cook_order, queue=QUEUE_COOK)
channel.basic_consume(on_message_callback=create_raw_recipe, queue=QUEUE_RAW_RECIPE)


if __name__ == "__main__":
    channel.start_consuming()
