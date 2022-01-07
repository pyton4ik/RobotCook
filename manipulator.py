"""
Abstract layer for manipulator controller
"""


class ManipulatorController:
    def go_to_pos(self, x, y, z):
        pass

    def get(self):
        pass

    def drop(self):
        pass

    def turn(self, degrees):
        pass
