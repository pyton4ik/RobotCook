from time import sleep
from dataclasses import dataclass

from errors import ErrorReceiptConfiguration, ProductNotFoundInDosator, NotReadyForCooking
from tools import ProcessingBasket, BoxBasket
import hardware
from dispenser import Dispenser
from processing_center import ProcessingCenter


def init_operations():
    operations = {p_center_config[0].lower(): ProcessingCenter(*p_center_config)
                  for p_center_config in hardware.processing_center_config}
    operations["oven"] = operations["grill"]
    operations["confection"] = operations["grill"]
    return operations


def init_products():
    products = {}
    for dispenser_config_elem in hardware.dispenser_config:
        for index, product in enumerate(dispenser_config_elem[0]):
            product_name = product.lower()
            products[product_name] = Dispenser(index, product_name, *dispenser_config_elem[1:])
    return products


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
        raise ErrorReceiptConfiguration(details="Not found operations with name {}". format(operation))

    return operations[operation_name]

class Operation:
    def __init__(self, product: str, operation: str, time: int):
        self.dispenser = get_product_obj(product)
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
        sleep(self.operation_time)
        self.p_center.open()
        self.manipulator.go_to_pos(*self.p_center.up_coordinates)
        self.p_center.close()
        self.manipulator.go_to_pos(*hardware.BASKET_PARKING_COORDINATES)
        self.tool.rotate()
        self.tool.rotate()

    def __call__(self, mode):
        self.tool.get()
        self.manipulator.go_to_pos(*self.dispenser.pick_up_point)
        self.dispenser.get_product()
        self._operation(mode)

        if self.p_center or not self.next_element_is_simple:
            self.tool.parking()


@dataclass
class Recipe:
    def __init__(self, operations):
        self.operations = (Operation(*recipe_item) for recipe_item in operations)
        self._check_recipe()
        self._iter_index = None

    def __call__(self, mode):
        for operation in self.operations:
            operation()
        return True

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index <= len(self.operations) - 1:
            ret_val = self.operations[self._iter_index]
            self._iter_index += 1
            return ret_val

        raise StopIteration

    def _check_recipe(self):
        if not self.operations:
            raise ErrorReceiptConfiguration(details="Receipt is null")

        not_enough_products_arr = [recipe_obj.dispenser.name for recipe_obj in self.operations
                                   if not recipe_obj.dispenser.is_have_required_amount]
        if not_enough_products_arr:
            raise NotReadyForCooking(details="Not enough products {} for cooking".format(not_enough_products_arr))

    def next_element_is_simple(self):
        if self._iter_index + 1 > len(self.operations) - 1:
            return False

        return not self.operations[self._iter_index + 1].p_center
