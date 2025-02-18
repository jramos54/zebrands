from api.domain.entities.product import Product
from api.domain.ports.product_repository import ProductRepository
from api.adapters.secondary.repositories.product_repository_impl import ProductRepositoryImpl
from django.utils.timezone import now
from django.db.utils import IntegrityError
from api.infrastructure.models import ProductQuery
from api.models import User
from django.db.models import F


from typing import List, Optional

class ProductService:
    """Servicio de negocio para la gestión de productos."""

    def __init__(self, product_repo: ProductRepository = None):
        """Inyectar la implementación concreta de `ProductRepository`."""
        self.product_repo = product_repo or ProductRepositoryImpl() 

    def get_product(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto por su ID."""
        return self.product_repo.get_by_id(product_id)

    def list_products(self, filters: dict) -> List[Product]:
        """Obtiene todos los productos aplicando filtros."""
        return self.product_repo.get_all(filters)

    def create_product(self, product_data):
        """Crea un producto y lo almacena en la base de datos."""
        product_data.setdefault("created_at", now())
        product_data.setdefault("updated_at", now())

        return self.product_repo.save(Product(**product_data))

    def update_product(self, instance: Product, validated_data: dict):
        """Actualiza un producto en la base de datos."""
        for key, value in validated_data.items():
            setattr(instance, key, value)  

        return self.product_repo.save(instance)

    def delete_product(self, product_id: int) -> None:
        """Elimina un producto por su ID."""
        product = self.get_product(product_id)
        if product:
            self.product_repo.delete(product)
            
    def increment_query_count(self, product_id, user):
        """Registra la consulta de un usuario anónimo en `ProductQuery`."""
        print(f"Intentando registrar consulta para producto {product_id} y usuario {user.id}")  
        try:
            query, created = ProductQuery.objects.get_or_create(
                product_id=product_id,
                user=user,
                defaults={"query_count": 1}
            )
            print(f"Registro creado: {created}, Query ID: {query.id if query else 'N/A'}")  
            
            if not created:
                print(f"Incrementando contador para el producto {product_id}")  
                ProductQuery.objects.filter(id=query.id).update(query_count=F("query_count") + 1)
                print(f"Contador incrementado correctamente")  
                
            print(f"Consulta registrada para el producto {product_id} por el usuario {user.id}")  
        except Exception as e:
            print(f"Error al registrar la consulta: {e}") 