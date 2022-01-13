"""
Common class for all Bathers
"""
from time import sleep

from errors import ProductNotFoundInDosator
from hardware import HardwareSouceDosator, HardwareSlicerController

ZERO_POINT = 34, 234, 531
CELL_SIZE_OFFSET = 34, 56
SOUCE_PRODUCTS_ARR = "mustard", "ketchup", "mayonnaise"
OPEN_WAIT_TIME = 0.4

DEFAULT_SLICE_QTY = 3
SLICER_PRODUCTS_ARR = "onion", "tomato", "pickle"
SLICER_ZERO_POINT = 123, 221, 673
SLICER_CELL_SIZE_OFFSET = 23, 32, 56


class Dosator():
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.zero_point = 0, 0, 0
        self.cell_size_offset = 0, 0, 0

    @property
    def pick_up_point(self):
        ret_val = [0, 0, 0]
        for dimension in range(3):
            ret_val[dimension] = self.zero_point[dimension] + self.cell_size_offset[0] * self.index

        return ret_val

    def dose(self):
        raise NotImplementedError('Define Method Dose for class {}'.format(self.__class__.__name__))


class DosatorController:
    def __init__(self, dosator_class, products):
        self._products = {product: dosator_class(product, products.index(product)) for product in products}

    def get_dosator(self, product: str):
        if product not in self._products:
            raise ProductNotFoundInDosator(product=product)
        return self._products[product]


class SouceDosator(Dosator):
    def __init__(self, name, index):
        super().__init__(name, index)
        self.zero_point = ZERO_POINT
        self.cell_size_offset = CELL_SIZE_OFFSET

    def dose(self):
        souce_dosator = HardwareSouceDosator(self.index)
        souce_dosator.apply_pressure()
        souce_dosator.open_valve()
        sleep(OPEN_WAIT_TIME)
        souce_dosator.close_valve()


class SouceDosatorController(DosatorController):
    def __init__(self):
        super().__init__(SouceDosator, SOUCE_PRODUCTS_ARR)


class Slicer(Dosator):
    hardware = HardwareSlicerController()

    def __init__(self, name, index):
        super().__init__(name, index)
        self.zero_point = SLICER_ZERO_POINT
        self.cell_size_offset = SLICER_CELL_SIZE_OFFSET

    def dose(self):
        for qty in range(DEFAULT_SLICE_QTY):
            self.hardware.slice()


class SlicerController(DosatorController):
    def __init__(self):
        super().__init__(Slicer, SLICER_PRODUCTS_ARR)
