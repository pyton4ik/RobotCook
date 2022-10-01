"""
Module for cooking operations.
Main class Recipe contain Operation's
Init hardware Products and Operations instances.
"""
import asyncio

import hardware
from dispenser import Dispenser
from errors import ErrorReceiptConfiguration
from errors import NotReadyForCooking
from errors import ProductNotFoundInDosator
from processing_center import ProcessingCenter
from tools import BoxBasket
from tools import ProcessingBasket


def init_operations():
    opers = {
        p_center_config[0].lower(): ProcessingCenter(*p_center_config)
        for p_center_config in hardware.processing_center_config
    }
    opers["oven"] = opers["grill"]
    opers["confection"] = opers["grill"]
    return opers


def init_products():
    prods = {}
    for dispenser_config_elem in hardware.dispenser_config:
        for index, product in enumerate(dispenser_config_elem[0]):
            product_name = product.lower()
            prods[product_name] = Dispenser(
                index, product_name, *dispenser_config_elem[1:]
            )
    return prods


products = init_products()
operations = init_operations()


def get_product_obj(product: str):
    product_name = product.lower()
    if product_name not in products:
        raise ProductNotFoundInDosator(product=product)

    return products[product_name]


def get_processing_center_obj(operation: str):
    if not operation:
        return None

    operation_name = operation.lower()
    if operation_name not in operations:
        raise ErrorReceiptConfiguration(
            details=f"Not found operations with name {operation}"
        )

    return operations[operation_name]


class Operation:
    """
    The sequence of Operation for preparing a Recipe.
    """

    def __init__(self, ingredient: str, operation: str, time: int, **_):
        self.dispenser = get_product_obj(ingredient)
        self.p_center = get_processing_center_obj(operation)
        self.operation_time = time
        self.operation = operation

        self.tool = BoxBasket()
        if self.operation:
            self.tool = ProcessingBasket()

        self.manipulator = hardware.ManipulatorController()

    def _operation(self):
        if not self.operation:
            return

        self.p_center.open()
        self.manipulator.go_to_pos(*self.p_center.coordinates)
        self.p_center.close()
        self.p_center.cooking(self.operation)
        asyncio.sleep(self.operation_time)
        self.p_center.open()
        self.manipulator.go_to_pos(*self.p_center.up_coordinates)
        self.p_center.close()
        self.manipulator.go_to_pos(*hardware.BASKET_PARKING_COORDINATES)
        self.tool.rotate()
        self.tool.rotate()

    def curr_call(self):
        self.tool.get()
        self.manipulator.go_to_pos(*self.dispenser.pick_up_point)
        self.dispenser.get_product()
        self._operation()
        self.tool.drop()

    def __call__(self):
        self.curr_call()


class Recipe:
    """
    Generate Operations list and cook this.
    """

    def __init__(self, oper):
        self.operations = (Operation(**dict(recipe_item)) for recipe_item in oper)
        self._check_recipe()

    async def __call__(self):
        for operation in self.operations:
            await operation()()
        return True

    def _check_recipe(self):
        if not self.operations:
            raise ErrorReceiptConfiguration(details="Receipt is null")

        not_enough_products_arr = [
            recipe_obj.dispenser.name
            for recipe_obj in self.operations
            if not recipe_obj.dispenser.is_have_required_amount
        ]
        if not_enough_products_arr:
            raise NotReadyForCooking(
                details="Not enough products {} for cooking".format(
                    not_enough_products_arr
                )
            )
