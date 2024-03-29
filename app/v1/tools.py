"""Инструмент

'Манипулятор' Ничего не делает без 'Инструментов'.
У манипулятора есть место хранения - parking_coordinates.

"""
from app.v1.hardware import ManipulatorController
from app.v1.schemas import Point


BASKET_PARKING_COORDINATES = Point(123, 321, 231)
PROCESSING_BASKET_PARKING_COORDINATES = Point(232, 282, 228)
UP_OFFSET = 100


class Tool:
    """Асбтрактный класс для всех инструментов."""

    def __init__(self):
        self.manipulator: ManipulatorController = ManipulatorController()
        self.parking_coordinates: Point = Point(0, 0, 0)

    def get(self):
        """Подводим манипулятор туда, где лежит Инструмент"""
        self.manipulator.go_to_pos(self.parking_coordinates)
        self.manipulator.get()

    def drop(self):
        """After every operation tools must be put to holder place"""
        self.manipulator.go_to_pos(self.parking_coordinates)
        self.manipulator.drop()


class BoxBasket(Tool):
    """
    Helper tools for transfer product from Dozator to Oven
    """

    def __init__(self):
        super().__init__()
        self.parking_coordinates = BASKET_PARKING_COORDINATES


class ProcessingBasket(Tool):
    """
    Main tools for cooking
    """

    def __init__(self):
        super().__init__()
        self.parking_coordinates = PROCESSING_BASKET_PARKING_COORDINATES

    def rotate(self):
        """
        Get product(s) and rotate him
        """
        self.manipulator.turn(180)
