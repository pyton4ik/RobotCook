"""
Module for manually launching a cluster of bots.
Bots qty for cluster in CLUSTER_QTY const
"""
import asyncio
import time
from math import ceil

from controller import cook_product_id
from controller import get_product
from database import SessionLocal

CLUSTER_QTY = 5
db = SessionLocal()
start = time.perf_counter()


def iteration(product_id):
    loop = asyncio.get_event_loop()
    tasks = [cook_product_id(db, product_id, index) for index in range(CLUSTER_QTY)]
    loop.run_until_complete(asyncio.wait(tasks))


def main(product_id, qty):
    start = time.perf_counter()
    product_obj = get_product(db, product_id)
    iterations = ceil(qty / CLUSTER_QTY)

    print(
        "\n{} \t Product: {} will be cooked ".format(
            time.perf_counter() - start, product_obj.name
        )
    )
    print(
        "{} \t Real qty {} ({} iterations) ".format(
            time.perf_counter() - start, iterations * CLUSTER_QTY, iterations
        )
    )

    for receipt_item in product_obj.receipts:
        print(
            "\t{}\t{}\t{}".format(
                receipt_item.ingredient, receipt_item.operation, receipt_item.wait_time
            )
        )

    for iter_index in range(iterations):
        iteration(product_id)
        print(f"Iteration {iter_index} was finished")


if __name__ == "__main__":
    product_id = int(input("Enter product_id"))
    qty = int(input("Enter qty"))
    main(product_id, qty)
