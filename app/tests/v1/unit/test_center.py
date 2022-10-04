from unittest import mock

import pytest

from app.v1 import hardware
from app.v1.processing_center import ProcessingCenter
from app.v1.schemas import Point
from app.v1.schemas import ProcessingCenterConfig


@pytest.mark.parametrize(
    "hardware_controller",
    [hardware.ProcessingCenterController, hardware.RosterProcessingCenterController],
)
@pytest.mark.parametrize(
    "angle,pickup_point", [(100, Point(297, 844, 345)), (150, Point(163, 716, 345))]
)
def test_center(monkeypatch, angle, pickup_point, hardware_controller):
    processing_center_obj = ProcessingCenter(
        ProcessingCenterConfig(
            name="MOCK CONTROLLER", angle=angle, object=hardware_controller
        )
    )

    assert processing_center_obj.config.name == "MOCK CONTROLLER"

    # Check Liskov substitution principle
    open_mock = mock.Mock()
    close_mock = mock.Mock()
    set_mode = mock.Mock()

    monkeypatch.setattr(hardware_controller, "open", open_mock)
    monkeypatch.setattr(hardware_controller, "close", close_mock)
    monkeypatch.setattr(hardware_controller, "cooking", set_mode)

    processing_center_obj.open()
    processing_center_obj.close()
    processing_center_obj.cooking("Grill")

    assert processing_center_obj.up_coordinates.x
    assert processing_center_obj.up_coordinates.y
    assert processing_center_obj.up_coordinates.z

    assert open_mock.mock_calls == [mock.call()]
    assert close_mock.mock_calls == [mock.call()]
    assert set_mode.mock_calls == [mock.call(mock.ANY)]
