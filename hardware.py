"""
Abstract layer for manipulator controller
"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


class HardwareSouceDosator():
    def __init__(self, index: int):
        self._index = index

    def apply_pressure(self):
        pass

    def open_valve(self):
        pass

    def close_valve(self):
        pass


class ManipulatorController:
    def go_to_pos(self, x, y, z):
        pass

    def get(self):
        pass

    def drop(self):
        pass

    def turn(self, degrees):
        pass


class HardwareSlicerController:
    def slice(self):
        pass


class RefregeratorComputerVision:
    def detect_qty(self):
        pass

    def get_product_coordinates(self, product_name: str):
        pass
