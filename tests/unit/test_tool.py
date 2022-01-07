from tools import Basket
from tools import Spatula
from tools import BASKET_PARKING_COORDINATES
from tools import SPATULA_PARKING_COORDINATES
from manipulator import ManipulatorController
import mock

def test_basket(monkeypatch):
    go_to_pos_mock = mock.Mock()
    get_mock = mock.Mock()
    drop_mock = mock.Mock()
    monkeypatch.setattr(ManipulatorController, "go_to_pos", go_to_pos_mock)
    monkeypatch.setattr(ManipulatorController, "get", get_mock)
    monkeypatch.setattr(ManipulatorController, "drop", drop_mock)
    basket = Basket()
    basket.get()

    assert go_to_pos_mock.mock_calls == [mock.call(*BASKET_PARKING_COORDINATES)]

