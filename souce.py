from time import sleep

from dosator import Dosator, DosatorController
from hardware import HardwareSouceDosator

ZERO_POINT = 34, 234, 531
CELL_SIZE_OFFSET = 34, 56
PRODUCTS_ARR = "mustard", "ketchup", "mayonnaise"
OPEN_WAIT_TIME = 0.4


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
        super().__init__(SouceDosator, PRODUCTS_ARR)
