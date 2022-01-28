# pylint: disable=missing-function-docstring
import mock
import pytest

from chef import Recipe
from errors import NotReadyForCooking, ErrorReceiptConfiguration, ProductNotFoundInDosator
from hardware import SouceDosatorController


@pytest.mark.parametrize("wrong_recipe_item,reises_class",
                         [({"ingredient": "ketchup", "operation": None, "time": None}, NotReadyForCooking),
                          ({"ingredient": "spam", "operation": None, "time": None}, ProductNotFoundInDosator),
                          ({"ingredient": "mayonnaise", "operation": "Nemo", "time": None}, ErrorReceiptConfiguration)])
def test_wrong_recipie_(monkeypatch, wrong_recipe_item, reises_class):
    if wrong_recipe_item["ingredient"] == "ketchup":
        monkeypatch.setattr(SouceDosatorController, "qty", 0)

    with pytest.raises(reises_class):
        Recipe([wrong_recipe_item])
