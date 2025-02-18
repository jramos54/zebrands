import pytest
from api.domain.entities.user import User
from api.application.user_service import UserService
from api.adapters.secondary.repositories.user_repository_impl import UserRepositoryImpl

@pytest.fixture
def user_repo():
    return UserRepositoryImpl()

@pytest.fixture
def user_service(user_repo):
    return UserService(user_repo)

def test_create_user(user_service):
    user = User(
        id=1, username="admin", email="admin@example.com",
        password="hashedpassword", role="admin",
        is_active=True, created_at=None, updated_at=None
    )
    saved_user = user_service.create_user(user)
    assert saved_user.email == "admin@example.com"

def test_get_user_not_found(user_service):
    user = user_service.get_user(999)
    assert user is None
