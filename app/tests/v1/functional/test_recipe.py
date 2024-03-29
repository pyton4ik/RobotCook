import csv
from pathlib import Path

import pytest

from app.v1.chef import Recipe


@pytest.fixture
def csv_receipt_list():
    csv_file_path = (
        Path(__file__).parent.parent.parent.parent.parent / "datas" / "recipes.csv"
    )
    with open(str(csv_file_path)) as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)
        return list(reader)


def test_recipes(csv_receipt_list):
    receipt_names = {
        line["name"] for line in csv_receipt_list if line["name"] != "name"
    }
    for receipt_name in receipt_names:
        Recipe([line for line in csv_receipt_list if line["name"] == receipt_name])
