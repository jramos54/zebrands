from abc import ABC, abstractmethod
from typing import List, Optional
from api.domain.entities.product import Product

class ProductRepository(ABC):
    """Interfaz abstracta para la gestión de productos en la base de datos."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Product]:
        """Obtiene un producto por su ID."""
        pass

    @abstractmethod
    def get_all(self, filters: dict) -> List[Product]:
        """Obtiene una lista de productos con filtros opcionales."""
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Guarda o actualiza un producto en la base de datos."""
        pass

    @abstractmethod
    def delete(self, product: Product) -> None:
        """Elimina un producto de la base de datos."""
        pass
