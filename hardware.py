"""
Abstract layer for manipulator controller
"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from time import sleep

from errors import ErrorReceiptConfiguration

SOUCE_OPEN_WAIT_TIME = 0

product_portion_qty_dict = {
    "onion": 15,
    "tomato": 15,
    "pickle": 15,
    "mustard": 5,
    "ketchup": 5,
    "mayonnaise": 5,
}


class ManipulatorController:
    def go_to_pos(self, x, y, z):
        pass

    def get(self):
        pass

    def drop(self):
        pass

    def turn(self, degrees):
        pass


class DosatorController:
    def __init__(self, index: int):
        self._index = index

    def get_product(self):
        ...

    @property
    def qty(self):
        return self._index ** 6


class BoxDosatorController(DosatorController):
    ...


class SouceDosatorController(DosatorController):
    def get_product(self):
        self._apply_pressure()
        self._open_valve()
        sleep(SOUCE_OPEN_WAIT_TIME)
        self._close_valve()

    def _apply_pressure(self):
        ...

    def _open_valve(self):
        ...

    def _close_valve(self):
        ...


class SlicerDosatorController(DosatorController):
    def get_product(self):
        for i in range(3):
            self.slice()

    def slice(self):
        ...


class RefrigeratorDosatorController(DosatorController):
    ...


class BreadDosatorController(DosatorController):
    ...


BOX_PRODUCTS_ARR = "s", "m", "l"
SOUCE_PRODUCTS_ARR = "mustard", "ketchup", "mayonnaise"
SLICER_PRODUCTS_ARR = "onion", "tomato", "pickle"
BREAD_PRODUCTS_ARR = "bun top", "bun bottom", "hot dog"


dispenser_config = [
    (BOX_PRODUCTS_ARR, 0, 5, BoxDosatorController),
    (BREAD_PRODUCTS_ARR, 15, 5, BreadDosatorController),
    (SLICER_PRODUCTS_ARR, 30, 5, SlicerDosatorController),
    (SOUCE_PRODUCTS_ARR, 45, 5, SouceDosatorController),
]


class ProcessingCenterController():
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
                            ("Boiling", 120, ProcessingCenterController),
                            ("Fryer", 150, ProcessingCenterController)]
