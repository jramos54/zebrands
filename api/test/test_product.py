import pytest
from api.domain.entities.product import Product
from api.application.product_service import ProductService
from api.adapters.secondary.repositories.product_repository_impl import ProductRepositoryImpl

@pytest.fixture
def product_repo():
    return ProductRepositoryImpl()

@pytest.fixture
def product_service(product_repo):
    return ProductService(product_repo)

def test_create_product(product_service):
    product = Product(
        id=1, sku="P001", name="Producto 1", price=10.0,
        brand="MarcaX", category="Categoria1", stock=100,
        short_description="Breve", long_description="Larga",
        is_active=True, created_at=None, updated_at=None
    )
    saved_product = product_service.create_product(product)
    assert saved_product.name == "Producto 1"

def test_get_product_not_found(product_service):
    product = product_service.get_product(999)
    assert product is None
