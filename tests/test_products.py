import pytest
from src.core import InventoryManager
from src.models import Product

@pytest.fixture
def manager(tmp_path):
    db_path = tmp_path / "test.db"
    return InventoryManager(str(db_path))

def test_add_product(manager):
    product_id = manager.add_product("Chocolate Ice Pop", 100, 2.5)
    product = manager.get_product(product_id)
    assert product.name == "Chocolate Ice Pop"
    assert product.quantity == 100
    