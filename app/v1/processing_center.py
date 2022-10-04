"""Место обработки продукта."""
from dataclasses import dataclass
from dataclasses import replace as dataclass_replace

from app.v1 import hardware
from app.v1.dispenser import OrbitingElement
from app.v1.errors import ErrorReceiptConfiguration
from app.v1.schemas import Point
from app.v1.schemas import ProcessingCenterConfig


@dataclass  # Современные штучки
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

    config: ProcessingCenterConfig

    def open(self):
        self.hardware.open()

    def cooking(self, mode):
        self.hardware.cooking(mode)

    def close(self):
        self.hardware.close()

    @property  # Современные штучки
    def up_coordinates(self) -> Point:
        ret_val = dataclass_replace(self.coordinates)
        ret_val.y -= hardware.UP_OFFSET
        return ret_val


class ProcessingCentersController:
    opers: dict[str, ProcessingCenter]

    def __int__(self):
        opers = {
            p_center_config[0].lower(): ProcessingCenter(p_center_config)
            for p_center_config in hardware.processing_center_config
        }
        opers["oven"] = opers["grill"]
        opers["confection"] = opers["grill"]
        return opers

    @classmethod  # Современные штучки
    def get(cls, operation: str) -> ProcessingCenter:
        if not operation:
            return None

        operation_name = operation.lower()
        if operation_name not in cls.opers:
            raise ErrorReceiptConfiguration(
                details=f"Not found operations with name {operation}"
            )

        return cls.opers[operation_name]


processing_centers_controller = ProcessingCentersController()
