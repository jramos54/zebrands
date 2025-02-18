from api.domain.entities.log_entry import LogEntry
from api.domain.ports.user_repository import UserRepository
from api.domain.ports.product_repository import ProductRepository
from typing import List, Optional
from datetime import datetime
from api.adapters.secondary.repositories.log_repository_impl import LogRepositoryImpl
from api.adapters.secondary.repositories.product_repository_impl import ProductRepositoryImpl
from api.infrastructure.models import ProductQuery
from api.domain.ports.log_repository import LogRepository
from django.db.models import F



class LogService:
    """Servicio para gestionar los registros de cambios en el sistema."""

    def __init__(self, user_repo: UserRepository = None, product_repo: ProductRepository = None, log_repo: LogRepository = None):
        self.user_repo = user_repo or LogRepositoryImpl()
        self.product_repo = product_repo or ProductRepositoryImpl()
        self.log_repo = log_repo if log_repo else LogRepositoryImpl()

    def log_action(self, admin_id: int, target_id: int, action: str, changes: dict) -> LogEntry:
        """Registra una acción en el sistema."""
        log_entry = LogEntry(
            id=0,
            admin_id=admin_id,
            target_id=target_id,
            action=action,
            changes=changes,
            created_at=datetime.utcnow(),  
        )
        self.log_repo.save(log_entry)
        return log_entry  

    def list_logs(self, filters: dict) -> List[LogEntry]:
        """Obtiene una lista de registros filtrados."""
        logs = self.log_repo.get_logs(filters)
        return logs if logs else [] 

    def get_anonymous_queries(self, product_id=None):
        """Obtiene el número de consultas realizadas por usuarios anónimos para un producto específico o todos."""
        query = ProductQuery.objects.filter(user__role="anonymus")

        if product_id:
            query = query.filter(product_id=product_id)

        return list(query.values("product_id", "user_id", "query_count"))

    def log_product_action(self, product_id: int, user_id: int, action: str, changes: dict = None):
        """Registra una acción sobre un producto."""
        if changes is None:
            changes = {}

        log_entry = LogEntry(
            id=0,
            admin_id=user_id,
            target_id=product_id,
            action=action,
            changes=changes,
            created_at=datetime.utcnow(),
        )
        self.log_repo.save(log_entry)
    
    def get_log(self, log_id: int) -> Optional[LogEntry]:
        """Obtiene un log por su ID."""
        return self.log_repo.get_by_id(log_id)
