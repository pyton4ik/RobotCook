"""
This file contain hardware constants and hardware adapters for all devices.
"""
# pylint: disable=missing-function-docstring
# pylint: disable=no-self-use
# pylint: disable=unused-argument
import asyncio

from errors import ErrorReceiptConfiguration

SOUCE_OPEN_WAIT_TIME = 300
UP_OFFSET = 100
BASKET_PARKING_COORDINATES = 100, 200, 300

product_portion_qty_dict = {
    "onion": 15,
    "tomato": 15,
    "pickle": 15,
    "mustard": 5,
    "ketchup": 5,
    "mayonnaise": 5,
}


class ManipulatorController:
    """
    This is a main part or system.
    Robot Arm manipulator.
    Delivers products to the box and processing centers.
    """
    def go_to_pos(self, x, y, z):
        ...

    def get(self):
        """Get tool ex. Basket"""
        ...

    def drop(self):
        """Drop tool ex. Basket"""
        ...

    def turn(self, degrees):
        """Rorate tool for degree"""
        ...


class DosatorController:
    """
    Common pattern for all dispensers
    Based Design pattern "Adapter"
    """
    def __init__(self, index: int):
        self._index = index

    def get_product(self):
        ...

    @property
    def qty(self):
        return 100500


class SouceDosatorController(DosatorController):
    async def get_product(self):
        self._apply_pressure()
        self._open_valve()
        await asyncio.sleep(SOUCE_OPEN_WAIT_TIME)
        self._close_valve()

    def _apply_pressure(self):
        ...

    def _open_valve(self):
        ...

    def _close_valve(self):
        ...


class SlicerDosatorController(DosatorController):
    def get_product(self):
        for _ in range(3):
            self.slice()

    def slice(self):
        ...


BOX_PRODUCTS_ARR = "box s", "box m", "box l"
SOUCE_PRODUCTS_ARR = "mustard", "ketchup", "mayonnaise"
SLICER_PRODUCTS_ARR = "onion", "tomato", "pickle"
BREAD_PRODUCTS_ARR = "bun top", "bun bottom", "hot dog bun"
REFRIGERATOR_PRODUCTS_ARR = "burger", "cheese", "sausage", "fries"
MASH_PRODUCTS_ARR = "mashed potatoes", "mashed beans"

dispenser_config = [
    (BOX_PRODUCTS_ARR, 0, 5, DosatorController),
    (BREAD_PRODUCTS_ARR, 15, 5, DosatorController),
    (SLICER_PRODUCTS_ARR, 30, 5, SlicerDosatorController),
    (SOUCE_PRODUCTS_ARR, 45, 5, SouceDosatorController),
    (REFRIGERATOR_PRODUCTS_ARR, 75, 7, DosatorController),
    (MASH_PRODUCTS_ARR, 75, 7, DosatorController),
]


class ProcessingCenterController():
    """
    Common pattern for all Processing Centers.
    Based Design pattern "Adapter".
    Redefine common methods with hardware needs.
    """
    def open(self):
        ...

    def close(self):
        ...

    def cooking(self, mode):
        ...


class RosterProcessingCenterController(ProcessingCenterController):
    def set_mode(self, mode):
        if mode == "Grill":
            self.turn_ten(1)
            self.turn_ten(2)
        elif mode == "Oven":
            self.turn_ten(1)
            self.turn_ten(2)
            self.turn_fun()
        elif mode == "Confection":
            self.turn_ten(2)
            self.turn_fun()
        else:
            raise ErrorReceiptConfiguration(details="Wrong Roster mode {}".format(mode))

    def turn_ten(self, index):
        ...

    def turn_fun(self):
        ...


processing_center_config = [("Grill", 100, RosterProcessingCenterController),
                            ("Warm", 120, ProcessingCenterController),
                            ("Fryer", 150, ProcessingCenterController)]
