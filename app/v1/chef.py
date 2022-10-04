"""
Module for cooking operations.
Main class Recipe contain Operation's
Init hardware Products and Operations instances.
"""
import asyncio

from app.v1 import hardware
from app.v1.dispenser import dispensers_controller
from app.v1.errors import ErrorReceiptConfiguration
from app.v1.errors import NotReadyForCooking
from app.v1.processing_center import processing_centers_controller
from app.v1.tools import BoxBasket
from app.v1.tools import ProcessingBasket


class Operation:
    """Операция для приготовления 'Продукта'

    Возможно нужно отрефакторить под Порождающий шаблон "Builder"? Современные штучки
    """

    def __init__(self, ingredient: str, operation: str, time: int, **_):

        self.dispenser = dispensers_controller.get(ingredient)
        self.p_center = processing_centers_controller.get(operation)
        self.operation_time = time
        self.operation = operation

        self.tool = BoxBasket()
        if self.operation:
            self.tool = ProcessingBasket()

        self.manipulator = hardware.ManipulatorController()

    def _cook(self):
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

    def __call__(self):
        self.tool.get()
        # Идем к диспенсеру
        self.manipulator.go_to_pos(*self.dispenser.pick_up_point)
        # Получаем продукт
        self.dispenser.get_product()
        # И готовим его
        self._cook()
        # Кладем корзину на место
        self.manipulator.go_to_pos(*hardware.BASKET_PARKING_COORDINATES)
        self.tool.rotate()
        self.tool.rotate()
        # Кладем инструмент на место
        self.tool.drop()


class Recipe:
    """Рецепт - список 'Операций' для приготовления продукта."""

    def __init__(self, oper):
        self.operations = (Operation(**dict(recipe_item)) for recipe_item in oper)
        self._check_recipe()

    async def __call__(self):
        for operation in self.operations:
            await operation()()
        return True

    def _check_recipe(self):
        """Перед началом приготовления опрашиваем железо на предмен наличия продуктов"""

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
