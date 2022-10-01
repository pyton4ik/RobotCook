import pytest

from app.v1.adapters.adapter_asyncio import main
from app.v1.errors import ProductNotFound


def test_main(db_init_products_dict):
    main(1, 13)


def test_raise_main(db_init_products_dict):
    with pytest.raises(ProductNotFound):
        main(555, 15)
