from abc import ABC, abstractmethod

class NotificationService(ABC):
    """Interfaz abstracta para el envío de notificaciones."""

    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Envía un correo electrónico a un usuario."""
        pass
