from dispenser import OrbitingElement
import hardware


class ProcessingCenter(OrbitingElement):
    def __init__(self, name, angle, hardware_class):
        self.name = name
        self._angle = angle
        self.hardware = hardware_class()

    def open(self):
        self.hardware.open()

    def close(self):
        self.hardware.close()

    def cooking(self, mode):
        self.hardware.cooking(mode)

    def up_coordinates(self):
        return self.coordinates[0:2, self.coordinates[3] - hardware.UP_OFFSET]
