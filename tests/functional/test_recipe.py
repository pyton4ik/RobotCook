import csv
import pytest
from pathlib import Path

from chef import Recipe

@pytest.fixture
def csv_receipt_list():
    csv_file_path = Path(__file__).parent.parent.parent / 'recipes.csv'
    with open(str(csv_file_path)) as csvfile:
        return list(csv.reader(csvfile))

def test_recipes(csv_receipt_list):
    receipt_names = {line[0] for line in csv_receipt_list}
    for receipt_name in receipt_names:
        Recipe([line[1:] for line in csv_receipt_list if line[0]==receipt_name])
