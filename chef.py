from time import sleep
from cnc import ControllCenter
from errors import ErrorReceiptConfiguration, ProductNotFoundInDosator, NotReadyForCooking
from tools import ProcessingBasket, BoxBasket
import hardware
from dispenser import Dispenser
from processing_center import ProcessingCenter


class Operation():
    def __init__(self,
                 ingredient_dispenser_obj: Dispenser,
                 processing_center_obj: ProcessingCenter,
                 operation_time):
        self.dispenser = ingredient_dispenser_obj
        self.p_center = processing_center_obj
        self.operation_time = operation_time

        self.tool = BoxBasket()
        if self.operation:
            self.tool = ProcessingBasket()

        self.manipulator = hardware.ManipulatorController()

    def _operation(self, mode):
        if not self.operation:
            return

        self.p_center.open()
        self.manipulator.go_to_pos(self.p_center.coordinates)
        self.p_center.close()
        self.p_center.cooking(self.operation)
        sleep(self.operation_time)
        self.p_center.open()
        self.manipulator.go_to_pos(self.p_center.up_coordinates)
        self.p_center.close()
        self.manipulator.go_to_pos(hardware.BASKET_PARKING_COORDINATES)
        self.tool.rotate()
        self.tool.rotate()

    def cooking(self, mode):
        self.tool.get()
        self.manipulator.go_to_pos(self.dispenser.pick_up_point)
        self.dispenser.get_product()
        self._operation(mode)
        self.tool.parking()


class ChiefCooker:
    def __init__(self):
        self.cnc = ControllCenter()
        self.manipulator = hardware.ManipulatorController()

        self._init_products()
        self._init_processing_centers()

    def _init_products(self):
        for dispenser_config_elem in hardware.dispenser_config:
            products = dispenser_config_elem
            for index, product in enumerate(products):
                product_name = product.lower()
                self._products[product_name] = Dispenser(index, product_name, *dispenser_config_elem[1:])

    def _init_processing_centers(self):
        for name, angle, hardware_class_name in hardware.processing_center_config:
            self._processing_centers[name.lower()] = ProcessingCenter(name, angle, hardware_class_name)

        self._processing_centers["oven"] = self._processing_centers["grill"]
        self._processing_centers["confection"] = self._processing_centers["grill"]

    def _get_product_obj(self, product: str):
        product_name = product.lower()
        if product_name not in self._products:
            raise ProductNotFoundInDosator(product=product)

        return self._products[product_name]

    def _get_processing_center_obj(self, name: str):
        if not name:
            return None

        center_name = name.lower()
        if center_name not in self._processing_centers:
            raise ErrorReceiptConfiguration(details="Not found processing center with name {}". format(name))

        return self._processing_centers[center_name]

    def _check_recipe(self, recipe: list):
        if not recipe:
            raise ErrorReceiptConfiguration(details="Receipt is null")

        qty_alarm_products_arr = [recipe_step["product"] for recipe_step in recipe
                                  if not self._get_product_obj(recipe_step["product"]).is_have_required_amount]
        if qty_alarm_products_arr:
            message = "No required quantity for products".format(qty_alarm_products_arr)
            self.cnc.alarm_notification(message)
            raise NotReadyForCooking(details=message)

    def cook_to_to_recipe(self, recipe: list):
        self._check_recipe(recipe)
        for recipe_step in recipe:
            Operation(self._get_product_obj(recipe["product"]),
                      self._get_processing_center_obj(recipe["operation"]),
                      recipe["time"]).cooking(recipe["operation"])
