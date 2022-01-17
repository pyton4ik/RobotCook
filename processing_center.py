from dispenser import OrbitingElement
import hardware

class ProcessingCenter(OrbitingElement):
    def __init__(self, angle, hardware_class):
        self._angle = angle
        self.hardware_class = hardware_class

    def open(self):
        self.hardware_class.open()

    def close(self):
        self.hardware_class.close()

    def cooking(self, mode):
        self.hardware_class.cooking(mode)

    def up_coordinates(self):
        return self.coordinates[0:2, self.coordinates[3] - hardware.UP_OFFSET]
