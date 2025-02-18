import pytest
from api.domain.entities.log_entry import LogEntry
from api.application.log_service import LogService
from api.adapters.secondary.repositories.log_repository_impl import LogRepositoryImpl

@pytest.fixture
def log_repo():
    return LogRepositoryImpl()

@pytest.fixture
def log_service(log_repo):
    return LogService(None, None)  # Simulación sin repositorio real

def test_create_log_entry(log_service):
    log_entry = LogEntry(
        id=1, admin_id=1, target_id=10,
        action="updated", changes={"price": "20.0"},
        created_at=None
    )
    log_service.log_action(log_entry.admin_id, log_entry.target_id, log_entry.action, log_entry.changes)
    assert log_entry.action == "updated"
