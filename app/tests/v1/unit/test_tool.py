from unittest import mock

import pytest

from app.v1.hardware import ManipulatorController
from app.v1.tools import BASKET_PARKING_COORDINATES
from app.v1.tools import BoxBasket
from app.v1.tools import PROCESSING_BASKET_PARKING_COORDINATES
from app.v1.tools import ProcessingBasket


@pytest.mark.parametrize(
    "tool_class,coordinates",
    [
        (BoxBasket(), BASKET_PARKING_COORDINATES),
        (ProcessingBasket(), PROCESSING_BASKET_PARKING_COORDINATES),
    ],
)
@pytest.mark.parametrize("operation", ("get", "drop"))
def test_tools_liskov_substitution_principle(
    monkeypatch, tool_class, coordinates, operation
):
    go_to_pos_mock = mock.Mock()
    operation_mock = mock.Mock()
    monkeypatch.setattr(ManipulatorController, "go_to_pos", go_to_pos_mock)
    monkeypatch.setattr(ManipulatorController, operation, operation_mock)

    getattr(tool_class, operation)()
    assert go_to_pos_mock.mock_calls == [mock.call(*coordinates)]
    assert operation_mock.mock_calls == [mock.call()]


def test_procc_basket_rotate(monkeypatch):
    operation_mock = mock.Mock()
    monkeypatch.setattr(ManipulatorController, "turn", operation_mock)

    ProcessingBasket().rotate()

    assert operation_mock.mock_calls == [mock.call(180)]
