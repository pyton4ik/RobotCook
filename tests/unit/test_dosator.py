"""
Common test for all dosators
"""
# pylint: disable=missing-function-docstring

import mock
import pytest

from dosator import Slicer, SlicerController
from dosator import SLICER_PRODUCTS_ARR
from dosator import SOUCE_PRODUCTS_ARR as souce_product_arr
from dosator import SouceDosator, SouceDosatorController
from errors import ProductNotFoundInDosator
from hardware import HardwareSouceDosator, HardwareSlicerController


@pytest.mark.parametrize("controller_class,product_name,pickup_pint",
                         [(SouceDosatorController, souce_product_arr[0], [34, 234, 531]),
                          (SlicerController, SLICER_PRODUCTS_ARR[0], [123, 221, 673])])
def test_dosator_liskov_substitution_principle(controller_class, product_name, pickup_pint):
    dosator_controller_obj = controller_class()
    dosator_obj = dosator_controller_obj.get_dosator(product_name)

    assert dosator_obj.index == 0
    assert dosator_obj.name == product_name
    assert dosator_obj.pick_up_point == pickup_pint

    with pytest.raises(ProductNotFoundInDosator):
        dosator_controller_obj.get_dosator("Bread")


@pytest.mark.parametrize("index", range(len(souce_product_arr)))
def test_souce_dosator(monkeypatch, index):
    mock_array = []
    for mock_attr in ["apply_pressure", "open_valve", "close_valve"]:
        mock_obj = mock.Mock()
        monkeypatch.setattr(HardwareSouceDosator, mock_attr, mock_obj)
        mock_array.append(mock_obj)

    souce_dosator = SouceDosator(index, str(index))
    souce_dosator.dose()

    for mock_obj in mock_array:
        assert mock_obj.mock_calls == [mock.call()]


@pytest.mark.parametrize("index", range(len(SLICER_PRODUCTS_ARR)))
def test_slicer(monkeypatch, index):
    slicer_controller_mock = mock.Mock()
    monkeypatch.setattr(HardwareSlicerController, "slice", slicer_controller_mock)

    slicer_controller = Slicer(index, str(index))
    slicer_controller.dose()

    assert slicer_controller_mock.mock_calls == [mock.call()] * 3
