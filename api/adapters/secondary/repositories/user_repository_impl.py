from api.domain.ports.user_repository import UserRepository
from api.domain.entities.user import User
from api.models import User as UserModel  

class UserRepositoryImpl(UserRepository):
    """Implementación de UserRepository usando Django ORM."""

    def get_by_id(self, id: int) -> User:
        """Obtiene un usuario por ID."""
        try:
            user = UserModel.objects.get(id=id)
            return self.to_entity(user)
        except UserModel.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> User:
        """Obtiene un usuario por email."""
        try:
            user = UserModel.objects.get(email=email)
            return self.to_entity(user)
        except UserModel.DoesNotExist:
            return None

    def get_all(self, filters: dict = None) -> list[User]:
        """Obtiene todos los usuarios con filtros opcionales."""
        users = UserModel.objects.filter(**filters) if filters else UserModel.objects.all()
        return [self.to_entity(user) for user in users]

    def save(self, user: User) -> User:
        """Guarda o actualiza un usuario en la base de datos y devuelve la entidad User."""
        user_data = self.to_model(user)  
        user_data.save()
        return self.to_entity(user_data)  

    def delete(self, user: User) -> None:
        """Elimina un usuario por ID."""
        UserModel.objects.filter(id=user.id).delete()

    def get_users_by_role(self, roles: list[str]) -> list[User]:
        """Consulta usuarios con ciertos roles."""
        users = UserModel.objects.filter(role__in=roles, is_active=True)
        return [self.to_entity(user) for user in users]

    def to_entity(self, user_model: UserModel) -> User:
        """Convierte un modelo Django `UserModel` a la entidad `User`."""
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            password=user_model.password,
            role=user_model.role,
            is_active=user_model.is_active,
            created_at=user_model.date_joined,  
            updated_at=user_model.last_login if user_model.last_login else user_model.date_joined,
            created_by=user_model.created_by.id if user_model.created_by else None,
            updated_by=user_model.updated_by.id if user_model.updated_by else None,
            last_login=user_model.last_login,
            token=user_model.token
        )

    def to_model(self, user: User) -> UserModel:
        """Convierte una entidad `User` en un modelo `UserModel` de Django."""
        user_model = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,  
            role=user.role,
            is_active=user.is_active,
            token=user.token
        )
        return user_model
