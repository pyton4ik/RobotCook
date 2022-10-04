"""Место обработчки продукта."""
import dataclasses

from app.v1 import hardware
from app.v1.dispenser import OrbitingElement
from app.v1.schemas import Point


class ProcessingCenter(OrbitingElement):
    """Цех обработки продуктов.

    Для разделения отвественности операции опускаем и поднимаем реализованы в
    классе Operation.

    Последовательность обработки:
        open
        опускаем
        cooking
        поднимаем
        close
    """

    def __init__(self, name, angle, hardware_class):
        """

        Args:
            name: Название цеха.
            angle: Угол расположения
            hardware_class: истанс класса железа
        """
        self.name = name
        self.angle = angle
        self.hardware = hardware_class()

    def open(self):
        self.hardware.open()

    def cooking(self, mode):
        self.hardware.cooking(mode)

    def close(self):
        self.hardware.close()

    @property  # Современные штучки
    def up_coordinates(self) -> Point:
        ret_val = dataclasses.replace(self.coordinates)
        ret_val.y -= hardware.UP_OFFSET
        return ret_val
