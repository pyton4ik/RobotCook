# pylint: disable=missing-function-docstring

import mock
import pytest

from processing_center import ProcessingCenter
import hardware

@pytest.mark.parametrize("hardware_controller",[hardware.ProcessingCenterController,
                                                hardware.RosterProcessingCenterController])
@pytest.mark.parametrize("angle,pickup_point",[(100, (163, 716, 345)),(150, (163, 716, 345))])
def test_dosator(monkeypatch, angle, pickup_point, hardware_controller):
    processing_center_obj = ProcessingCenter("MOCK CONTROLLER", angle, hardware_controller)

    assert processing_center_obj.name == "MOCK CONTROLLER"
    assert processing_center_obj.coordinates == pickup_point

    # Check Liskov substitution principle
    open_mock = mock.Mock()
    close_mock = mock.Mock()
    set_mode = mock.Mock()

    monkeypatch.setattr(hardware_controller, "open", open_mock)
    monkeypatch.setattr(hardware_controller, "close", close_mock)
    monkeypatch.setattr(hardware_controller, "set_mode", set_mode)

    processing_center_obj.hardware.open()
    processing_center_obj.hardware.close()
    processing_center_obj.hardware.set_mode("Grill")

    assert open_mock.mock_calls == [mock.call()]
    assert close_mock.mock_calls == [mock.call()]
    assert set_mode.mock_calls == [mock.call(mock.ANY)]