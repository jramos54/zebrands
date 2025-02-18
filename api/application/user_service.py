from api.domain.entities.user import User
from api.domain.ports.user_repository import UserRepository
from api.adapters.secondary.repositories.user_repository_impl import UserRepositoryImpl
from django.contrib.auth.hashers import make_password

from typing import List, Optional

class UserService:
    """Servicio de negocio para la gestión de usuarios."""

    def __init__(self, user_repo: UserRepository = None):
        """Inyecta una implementación concreta de UserRepository."""
        self.user_repo = user_repo or UserRepositoryImpl() 

    def get_user(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        return self.user_repo.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su email."""
        return self.user_repo.get_by_email(email)

    def list_users(self, filters: dict) -> List[User]:
        """Obtiene todos los usuarios aplicando filtros."""
        return self.user_repo.get_all(filters)

    def create_user(self, user: User) -> User:
        """Encripta la contraseña y guarda el usuario en la base de datos."""
        
        
        encrypted_password = make_password(user.password)  
        
        
        user_with_hashed_password = User(
            id=user.id,
            username=user.username,
            email=user.email,
            password=encrypted_password,  
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            created_by=user.created_by,
            updated_by=user.updated_by,
            last_login=user.last_login,
            token=user.token
        )
        
        return self.user_repo.save(user_with_hashed_password)  

    def update_user(self, user: User) -> User:
        """Actualiza un usuario existente."""
        return self.user_repo.save(user)

    def delete_user(self, user_id: int) -> None:
        """Elimina un usuario por su ID."""
        user = self.get_user(user_id)
        if user:
            self.user_repo.delete(user)
    
    def get_admin_emails(self):
        """Obtiene los correos de todos los administradores."""
        admins = self.user_repo.get_users_by_role(["admin", "super_admin"])
        return [admin.email for admin in admins]
