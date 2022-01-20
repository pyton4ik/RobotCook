# pylint: disable=missing-function-docstring
import mock
import pytest

from chef import Recipe
from errors import NotReadyForCooking, ErrorReceiptConfiguration, ProductNotFoundInDosator
from hardware import SouceDosatorController


@pytest.mark.parametrize("wrong_recipe_item,reises_class",
                         [(("ketchup", None, None), NotReadyForCooking),
                          (("spam", None, None), ProductNotFoundInDosator),
                          (("mayonnaise", "Nemo", None), ErrorReceiptConfiguration)])
def test_wrong_recipie_(monkeypatch, wrong_recipe_item, reises_class):
    if wrong_recipe_item[0] == "ketchup":
        monkeypatch.setattr(SouceDosatorController, "qty", 0)

    with pytest.raises(reises_class):
        Recipe([wrong_recipe_item])
