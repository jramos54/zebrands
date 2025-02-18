from api.domain.ports.product_repository import ProductRepository
from api.domain.entities.product import Product
from api.infrastructure.models import ProductModel
from django.db import IntegrityError


class ProductRepositoryImpl(ProductRepository):
    """Implementación de ProductRepository usando Django ORM."""

    def get_by_id(self, id: int) -> Product:
        try:
            product = ProductModel.objects.get(id=id)
            return self._convert_to_entity(product)
        except ProductModel.DoesNotExist:
            return None

    def get_all(self, filters: dict) -> list[Product]:
        products = ProductModel.objects.filter(**filters)
        return [self._convert_to_entity(product) for product in products]

    def save(self, product: Product) -> Product:
        """Guarda un producto en la base de datos y retorna la entidad Product."""
        product_data = {key: value for key, value in product.__dict__.items() if key != "_state"}

        try:
            product_model, _ = ProductModel.objects.update_or_create(id=product.id, defaults=product_data)
            return Product(**{
                "id": product_model.id,
                "name": product_model.name,
                "sku": product_model.sku,
                "price": product_model.price,
                "category": product_model.category,
                "brand": product_model.brand,
                "stock": product_model.stock,
                "short_description": product_model.short_description,
                "long_description": product_model.long_description,
                "is_active": product_model.is_active,
                "created_at": product_model.created_at,
                "updated_at": product_model.updated_at,
            })
        except IntegrityError as e:
            raise ValueError(f"Error al guardar el producto: {str(e)}")

    def delete(self, product: Product) -> None:
        ProductModel.objects.filter(id=product.id).delete()

    def _convert_to_entity(self, product_model):
        """🔹 Convierte un modelo de Django en una entidad Product."""
        product_data = {
            key: value for key, value in product_model.__dict__.items()
            if key != "_state"  
        }
        return Product(**product_data)
