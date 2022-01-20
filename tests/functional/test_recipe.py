import csv
import pytest

from chef import Recipe

@pytest.fixture
def csv_receipt_list():
    with open('recipes.csv') as csvfile:
        return csv.reader(csvfile)

def test_recipes(csv_receipt_list, recipe_name):
    receipt_names = {line[0] for line in csv_receipt_list}
    for receipt_name in receipt_names:
        Recipe([line[1:] for line in csv_receipt_list if line[0]==receipt_name])
