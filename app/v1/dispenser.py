"""Диспенсер

Место из которого поступают "Инградиент"ы. Распологаются по кругу от центра,
на одной высоте (DISPENSER_Z_COORD).
Так мы всегда можем вычислить 3D Координаты по только по одному параметру -
угол смещения, как в часах с одной стрелкой.
Продукты для подачи обработаны и расфасованы так что бы можно было
из подавать по гравитационному принципу.

Бывают следующих типов:
    Холодильник
        Здесь хранятся продукты, требующие хранения в холодильнике:
        Котлеты для бургеров, сыр и прочее.

    Слайсер
        Отсюда поступают уже нарезанные овощи: помидор, оругец, лук.

    Соус
        Кенчуп, майоне, горчица

    Пюре
        Картошечка
    Хлеб
        Хлеб для тостов, Булочки для бургеров (их 2 верхняя и нижняя)
"""
from math import cos
from math import sin

from app.v1 import hardware
from app.v1.errors import ProductNotFoundInDosator
from app.v1.schemas import Point

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

        return Point(x, y, DISPENSER_Z_COORD)


class Dispenser(OrbitingElement):
    """Диспенсеры сгруппированы по типу (соусы, овощи)."""

    def __init__(self, index, name, start_angle, elem_angle, hardware_class):
        """Диспенсеры сгруппированы по типу (соусы, овощи).

        Args:
            index: Порядковый номер в группе.
            name: Название.
            start_angle: Начальный угол.
            elem_angle: Расстояние между елементами.
            hardware_class: Инстанс контроллера железа.
        """
        self.name = name
        self.index = index

        self.start_group_angle = start_angle
        self.elements_angle = elem_angle

        self.hardware = hardware_class(self.index)

    @property
    def angle(self):
        return self.start_group_angle + self.index * self.elements_angle

    def get_product(self):
        return self.hardware.get_product()

    @property
    def is_have_required_amount(self) -> bool:
        """Перед началом приготовления нужно убедится что все продукты есть в наличии.
        Запрашиваем у Железа эту информацию.
        """
        return self.hardware.qty >= hardware.product_portion_qty_dict.get(self.name, 1)


class DispensersController:
    """Порождающие шаблон 'мультитон' Современные штучки"""

    products: dict[str, Dispenser] = {}

    def __int__(self):
        for dispenser_config_elem in hardware.dispenser_config:
            for index, product in enumerate(dispenser_config_elem[0]):
                product_name = product.lower()
                self.products[product_name] = Dispenser(
                    index, product_name, *dispenser_config_elem[1:]
                )

    @classmethod
    def get(self, product: str) -> Dispenser:
        product_name = product.lower()
        if product_name not in self.products:
            raise ProductNotFoundInDosator(product=product)

        return self.products[product_name]


dispensers_controller = DispensersController()
