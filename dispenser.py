"""
Common class for all Dispensers
"""
from math import sin, cos
import hardware

DISPENSER_Z_COORD = 345
ZERO_POINT = 500, 500
RADIUS = 400


class OrbitingElement:
    angle = -1

    @property
    def coordinates(self):
        """
        This method required angle attribute
        :return:
        """
        x = int(ZERO_POINT[0] + RADIUS * sin(self.angle))
        y = int(ZERO_POINT[1] + RADIUS * cos(self.angle))

        return (x, y, DISPENSER_Z_COORD)


class Dispenser(OrbitingElement):
    def __init__(self, index, name, start_angle, elem_angle, hardware_class):
        self.name = name
        self.index = index

        self.start_group_angle = start_angle
        self.elements_angle = elem_angle

        self.hardware = hardware_class

    @property
    def angle(self):
        return self.start_group_angle + self.index * self.elements_angle

    def dose(self):
        self.hardware.get_product(self.index)

    @property
    def is_have_required_amount(self) -> bool:
        """
        Consumption rate for weight products. Gets from product_portion_qty_dict.
        If the product is not presented in the product_portion_qty_dict dictionary, then it is considered piece.
        :return: bool
        """
        return self.hardware.get_qty(self.index) >= hardware.product_portion_qty_dict.get(self.name, 1)
