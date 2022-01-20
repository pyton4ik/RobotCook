import copy
from dispenser import OrbitingElement
import hardware


class ProcessingCenter(OrbitingElement):
    def __init__(self, name, angle, hardware_class):
        self.name = name
        self.angle = angle
        self.hardware = hardware_class()

    def open(self):
        self.hardware.open()

    def close(self):
        self.hardware.close()

    def cooking(self, mode):
        self.hardware.cooking(mode)

    @property
    def up_coordinates(self):
        ret_val = list(self.coordinates)
        ret_val[2] -= hardware.UP_OFFSET
        return tuple(ret_val)
