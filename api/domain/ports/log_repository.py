from abc import ABC, abstractmethod
from api.domain.entities.log_entry import LogEntry
from typing import List, Optional

class LogRepository(ABC):
    """Interfaz del repositorio de logs."""

    @abstractmethod
    def save(self, log: LogEntry) -> None:
        """Guarda un log en la base de datos."""
        pass

    @abstractmethod
    def get_by_id(self, log_id: int) -> Optional[LogEntry]:
        """Obtiene un log por su ID."""
        pass

    @abstractmethod
    def get_all(self, filters: dict) -> List[LogEntry]:
        """Obtiene todos los logs con filtros opcionales."""
        pass
