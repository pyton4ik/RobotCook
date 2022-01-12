"""
Common test for all dosators
"""
# pylint: disable=missing-function-docstring

import mock
import pytest

from souce import PRODUCTS_ARR as souce_product_arr
from souce import SouceDosator, SouceDosatorController
from hardware import HardwareSouceDosator


@pytest.mark.parametrize("controller_class,product_name,pickup_pint",
                         [(SouceDosatorController, souce_product_arr[0], [34, 234, 0]),
                          (SouceDosatorController, souce_product_arr[0], [34, 234, 0])])
def test_dosator_liskov_substitution_principle(controller_class, product_name, pickup_pint):
    dosator_controller_obj = controller_class()
    dosator_obj = dosator_controller_obj.get_dosator(product_name)

    assert dosator_obj.index == 0
    assert dosator_obj.name == product_name
    assert dosator_obj.pick_up_point == pickup_pint


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
