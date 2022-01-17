"""
Common test for all dosators
"""
# pylint: disable=missing-function-docstring

import mock
import pytest

from dispenser import Dispenser
import hardware

@pytest.mark.parametrize("hardware_dosator_controller",
                         [hardware.BoxDosatorController,
                         hardware.SouceDosatorController,
                         hardware.SlicerDosatorController,
                         hardware.RefrigeratorDosatorController,
                         hardware.BreadDosatorController])
@pytest.mark.parametrize("start_angle,elem_angle,pickup_point",
                         [(0, 5, (116, 613, 345)),
                          (15, 5, (865, 663, 345)),
                          (1, 30, (338, 865, 345)),
                          (1, 45, (860, 327, 345))])
@pytest.mark.parametrize("hardware_qty,is_have_amount",[(0, False),(100500, True)])
def test_dosator(monkeypatch, start_angle, elem_angle, pickup_point, hardware_dosator_controller,
                 hardware_qty, is_have_amount):
    dispenser_obj = Dispenser(1, "MOCK PRODUCT", start_angle, elem_angle, hardware_dosator_controller)

    assert dispenser_obj.index == 1
    assert dispenser_obj.name == "MOCK PRODUCT"
    assert dispenser_obj.coordinates == pickup_point

    get_product_mock = mock.Mock()
    get_qty = mock.Mock(return_value=hardware_qty)

    monkeypatch.setattr(hardware_dosator_controller, "get_product", get_product_mock)
    monkeypatch.setattr(hardware_dosator_controller, "get_qty", get_qty)

    # Check Liskov substitution principle
    dispenser_obj.get_product()
    assert dispenser_obj.is_have_required_amount == is_have_amount

    assert get_product_mock.mock_calls == [mock.call()]
    assert get_qty.mock_calls == [mock.call(mock.ANY)]


def test_souce_dosator(monkeypatch):
    mock_array = []
    for mock_attr in ["_apply_pressure", "_open_valve", "_close_valve"]:
        mock_obj = mock.Mock()
        monkeypatch.setattr(hardware.SouceDosatorController, mock_attr, mock_obj)
        mock_array.append(mock_obj)

    souce_dosator = Dispenser(0, "MOCK PRODUCT", 0, 0, hardware.SouceDosatorController)
    souce_dosator.get_product()

    for mock_obj in mock_array:
        assert mock_obj.mock_calls == [mock.call()]


def test_slicer(monkeypatch):
    slicer_controller_mock = mock.Mock()
    monkeypatch.setattr(hardware.SlicerDosatorController, "slice", slicer_controller_mock)

    slicer_controller = Dispenser(0, "MOCK PRODUCT", 0, 0, hardware.SlicerDosatorController)
    slicer_controller.get_product()

    assert slicer_controller_mock.mock_calls == [mock.call()] * 3
