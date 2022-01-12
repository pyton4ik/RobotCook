# pylint: disable=missing-function-docstring

import mock
import pytest

from manipulator import ManipulatorController
from tools import Basket
from tools import Spatula
from tools import BASKET_PARKING_COORDINATES
from tools import SPATULA_PARKING_COORDINATES


@pytest.mark.parametrize("tool_class,coordinates", [(Basket(), BASKET_PARKING_COORDINATES),
                                                    (Spatula(), SPATULA_PARKING_COORDINATES)])
@pytest.mark.parametrize("operation", ("get", "drop"))
def test_tools_liskov_substitution_principle(monkeypatch, tool_class, coordinates, operation):
    go_to_pos_mock = mock.Mock()
    operation_mock = mock.Mock()
    monkeypatch.setattr(ManipulatorController, "go_to_pos", go_to_pos_mock)
    monkeypatch.setattr(ManipulatorController, operation, operation_mock)

    getattr(tool_class, operation)()
    assert go_to_pos_mock.mock_calls == [mock.call(*coordinates)]
    assert operation_mock.mock_calls == [mock.call()]


def test_spatula_rotate(monkeypatch):
    operation_mock = mock.Mock()
    monkeypatch.setattr(ManipulatorController, "turn", operation_mock)

    Spatula().rotate()

    assert operation_mock.mock_calls == [mock.call(180)]
