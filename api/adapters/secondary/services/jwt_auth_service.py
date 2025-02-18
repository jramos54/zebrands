from api.domain.ports.auth_service import AuthService
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

import jwt
import datetime
import os

class JWTAuthService(AuthService):
    """Implementación de AuthService usando JWT."""

    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET", "supersecretkey")

    def authenticate_user(self, username, password):
        """Autentica un usuario y lo devuelve si es válido."""
        user = authenticate(username=username, password=password)
        if user:
            return user
        return None

    def login(self, username, password):
        """Autentica y genera tokens JWT."""
        user = self.authenticate_user(username, password)
        if user:
            refresh = RefreshToken.for_user(user)
            return {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
        return None

    def refresh(self, refresh_token):
        """Renueva el access_token usando un refresh_token válido."""
        try:
            refresh = RefreshToken(refresh_token)
            return str(refresh.access_token)
        except Exception:
            return None

    def logout(self, refresh_token):
        """Revoca el refresh token"""
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  
            return True
        except Exception as e:
            return False

    def validate_token(self, token: str) -> bool:
        try:
            jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            return False
