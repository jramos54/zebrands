from abc import ABC, abstractmethod
from typing import List, Optional
from api.domain.entities.user import User

class UserRepository(ABC):
    """Interfaz abstracta para la gestión de usuarios en la base de datos."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su correo electrónico."""
        pass

    @abstractmethod
    def get_all(self, filters: dict) -> List[User]:
        """Obtiene una lista de usuarios con filtros opcionales."""
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Guarda o actualiza un usuario en la base de datos."""
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        """Elimina un usuario de la base de datos."""
        pass
    
    def get_users_by_role(self, roles):
        """Debe ser implementado en la capa secundaria."""
        raise NotImplementedError
