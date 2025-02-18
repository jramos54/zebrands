from api.domain.entities.log_entry import LogEntry
from api.infrastructure.models import LogModel
from typing import List, Optional

class LogRepositoryImpl:
    """Manejo de logs usando Django ORM."""

    def save(self, log_entry: LogEntry) -> None:
        """Guarda un log en la base de datos."""
        LogModel.objects.create(
            admin_id=log_entry.admin_id,
            target_id=log_entry.target_id,
            action=log_entry.action,
            changes=log_entry.changes,
            created_at=log_entry.created_at,
        )

    def get_logs(self, filters: dict) -> list[LogEntry]:
        """Obtiene los logs de la base de datos aplicando filtros."""
        logs_queryset = LogModel.objects.all()

        # Aplica los filtros dinámicamente
        if "user_id" in filters:
            logs_queryset = logs_queryset.filter(admin_id=filters["user_id"])
        if "product_id" in filters:
            logs_queryset = logs_queryset.filter(target_id=filters["product_id"])
        if "action" in filters:
            logs_queryset = logs_queryset.filter(action=filters["action"])
        if "start_date" in filters:
            logs_queryset = logs_queryset.filter(created_at__gte=filters["start_date"])
        if "end_date" in filters:
            logs_queryset = logs_queryset.filter(created_at__lte=filters["end_date"])

        logs = [LogEntry(
            id=log.id,
            admin_id=log.admin_id,
            target_id=log.target_id,
            action=log.action,
            changes=log.changes,
            created_at=log.created_at,
        ) for log in logs_queryset]

        return logs
    
    def get_by_id(self, log_id: int) -> Optional[LogEntry]:
        """Obtiene un log específico por su ID."""
        try:
            log = LogModel.objects.get(id=log_id)
            return LogEntry(
                id=log.id,
                admin_id=log.admin_id,
                target_id=log.target_id,
                action=log.action,
                changes=log.changes,
                created_at=log.created_at,
            )
        except LogModel.DoesNotExist:
            return None
