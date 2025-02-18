from abc import ABC, abstractmethod
from typing import Optional

class AuthService(ABC):
    """Interfaz abstracta para la autenticación y gestión de sesiones."""

    @abstractmethod
    def login(self, username: str, password: str) -> Optional[str]:
        """Autentica a un usuario y devuelve un token JWT."""
        pass

    @abstractmethod
    def refresh(self, refresh_token: str) -> Optional[str]:
        """Renueva un token de acceso."""
        pass

    @abstractmethod
    def logout(self, token: str) -> None:
        """Cierra la sesión de un usuario invalidando su token."""
        pass

    @abstractmethod
    def validate_token(self, token: str) -> bool:
        """Valida un token JWT y devuelve su estado."""
        pass
