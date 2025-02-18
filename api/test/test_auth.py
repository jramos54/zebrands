import pytest
from api.application.auth_service import AuthServiceImpl
from api.adapters.secondary.services.jwt_auth_service import JWTAuthService

@pytest.fixture
def auth_service():
    return AuthServiceImpl()

def test_login_valid(auth_service):
    token = auth_service.login("admin@example.com", "password")
    assert token is not None

def test_login_invalid(auth_service):
    token = auth_service.login("user@example.com", "wrongpassword")
    assert token is None

def test_token_validation(auth_service):
    token = auth_service.login("admin@example.com", "password")
    assert auth_service.validate_token(token) is True
