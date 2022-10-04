"""Common test for all dosators"""
from unittest import mock

import pytest

from app.v1 import hardware
from app.v1.dispenser import Dispenser
from app.v1.schemas import Point


# Современные штучки
@pytest.mark.parametrize(
    "hardware_dosator_controller",
    [hardware.SouceDosatorController, hardware.SlicerDosatorController],
)
@pytest.mark.parametrize(
    "start_angle,elem_angle,pickup_point",
    [
        (0, 5, Point(116, 613, 345)),
        (15, 5, Point(865, 663, 345)),
        (1, 30, Point(338, 865, 345)),
        (1, 45, Point(860, 327, 345)),
    ],
)
@pytest.mark.parametrize("hardware_qty,is_have_amount", [(0, False), (100500, True)])
def test_dosator(
    monkeypatch,
    start_angle,
    elem_angle,
    pickup_point,
    hardware_dosator_controller,
    hardware_qty,
    is_have_amount,
):
    dispenser_obj = Dispenser(
        1, "MOCK PRODUCT", start_angle, elem_angle, hardware_dosator_controller
    )

    assert dispenser_obj.index == 1
    assert dispenser_obj.name == "MOCK PRODUCT"
    assert dispenser_obj.coordinates == pickup_point

    get_product_mock = mock.Mock()

    monkeypatch.setattr(hardware_dosator_controller, "get_product", get_product_mock)
    monkeypatch.setattr(hardware_dosator_controller, "qty", hardware_qty)

    # Check Liskov substitution principle
    dispenser_obj.get_product()
    assert dispenser_obj.is_have_required_amount == is_have_amount
    assert get_product_mock.mock_calls == [mock.call()]


async def test_souce_dosator(monkeypatch, path_mock_delay):
    mock_array = []
    for mock_attr in ["_apply_pressure", "_open_valve", "_close_valve"]:
        mock_obj = mock.Mock()
        monkeypatch.setattr(hardware.SouceDosatorController, mock_attr, mock_obj)
        mock_array.append(mock_obj)

    souce_dosator = Dispenser(0, "MOCK PRODUCT", 0, 0, hardware.SouceDosatorController)
    await souce_dosator.get_product()


def test_slicer(monkeypatch):
    slicer_controller_mock = mock.Mock()
    monkeypatch.setattr(
        hardware.SlicerDosatorController, "slice", slicer_controller_mock
    )

    slicer_controller = Dispenser(
        0, "MOCK PRODUCT", 0, 0, hardware.SlicerDosatorController
    )
    slicer_controller.get_product()

    assert slicer_controller_mock.mock_calls == [mock.call()] * 3
