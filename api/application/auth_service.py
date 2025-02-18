from api.domain.ports.auth_service import AuthService
from api.domain.ports.user_repository import UserRepository
from typing import Optional
import jwt
import datetime
import os
from django.contrib.auth.hashers import make_password
import uuid
from datetime import datetime, timedelta
from api.adapters.secondary.services.email_service import EmailService
from api.models import User
from django.core.exceptions import ObjectDoesNotExist




class AuthServiceImpl(AuthService):
    """Servicio de autenticación usando JWT."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.secret_key = os.getenv("JWT_SECRET", "supersecretkey")

    def login(self, username: str, password: str) -> Optional[str]:
        """Autentica al usuario y devuelve un token JWT."""
        user = self.user_repo.get_by_email(username)
        if user and user.password == password:  # Debería ser un hash real
            payload = {
                "user_id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            }
            return jwt.encode(payload, self.secret_key, algorithm="HS256")
        return None

    def refresh(self, refresh_token: str) -> Optional[str]:
        """Renueva un token de acceso."""
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=["HS256"])
            new_payload = {
                "user_id": payload["user_id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            }
            return jwt.encode(new_payload, self.secret_key, algorithm="HS256")
        except jwt.ExpiredSignatureError:
            return None

    def logout(self, token: str) -> None:
        """Invalida el token del usuario (no almacenado en DB)."""
        pass

    def validate_token(self, token: str) -> bool:
        """Valida un token JWT y devuelve su estado."""
        try:
            jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            return False

class AuthService:
    def __init__(self):
        self.email_service = EmailService()

    def forgot_password(self, email: str):
        """Genera un token de recuperación de contraseña y lo envía por correo."""
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return {"error": "No existe un usuario con este correo."}, 404
        
        reset_token = str(uuid.uuid4())  
        user.reset_token = reset_token
        user.reset_token_expiration = datetime.now() + timedelta(hours=1)  
        user.save()

        self.email_service.send_email(
            to=email,
            subject="Recuperación de Contraseña",
            body=f"Usa este token para restablecer tu contraseña: {reset_token}"
        )

        return {"message": "Se ha enviado un correo con instrucciones."}, 200

    def reset_password(self, token: str, new_password: str):
        """Permite restablecer la contraseña con el token válido."""
        try:
            user = User.objects.get(reset_token=token)
        except ObjectDoesNotExist:
            return {"error": "Token inválido o expirado."}, 400
        
        if user.reset_token_expiration < datetime.now():
            return {"error": "El token ha expirado."}, 400

        user.password = make_password(new_password)
        user.reset_token = None
        user.reset_token_expiration = None
        user.save()

        return {"message": "Contraseña actualizada correctamente."}, 200
