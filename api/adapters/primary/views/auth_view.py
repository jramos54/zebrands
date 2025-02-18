from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.adapters.primary.serializers.auth_serializer import AuthSerializer
from api.application.auth_service import AuthService
from api.adapters.secondary.services.jwt_auth_service import JWTAuthService
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    """Vista para iniciar sesión y obtener token JWT"""
    authentication_classes = []  
    permission_classes = []    
    auth_service = JWTAuthService()

    @swagger_auto_schema(
        request_body=AuthSerializer,
        responses={200: "Tokens generados", 400: "Credenciales inválidas"}
    )
    def post(self, request):
        """Autenticación de usuario y generación de tokens JWT (access y refresh)."""
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user = self.auth_service.authenticate_user(
                serializer.validated_data["username"], 
                serializer.validated_data["password"]
            )

            if user:
                # Generar access y refresh tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh)
                }, status=status.HTTP_200_OK)
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """Vista para cerrar sesión e invalidar token"""
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]
    auth_service = JWTAuthService()  

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh_token"],
            properties={
                "refresh_token": openapi.Schema(type=openapi.TYPE_STRING, description="Token de actualización")
            }
        ),
        responses={200: "Sesión cerrada", 400: "Token inválido"}
    )
    def post(self, request):
        """Cerrar sesión e invalidar el refresh token."""
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Se requiere un refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        is_revoked = self.auth_service.logout(refresh_token)

        if is_revoked:
            return Response({"message": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Token inválido o ya expirado"}, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    """Vista para refrescar token de autenticación"""
    auth_service = JWTAuthService()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"refresh_token": openapi.Schema(type=openapi.TYPE_STRING)}
        ),
        responses={200: "Token renovado", 400: "Token inválido"}
    )
    def post(self, request):
        """Renovar el token de autenticación."""
        refresh_token = request.data.get("refresh_token")
        new_token = self.auth_service.refresh(refresh_token)
        if new_token:
            return Response({"token": new_token}, status=status.HTTP_200_OK)
        return Response({"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    auth_service = AuthService()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="Correo del usuario")
            }
        ),
        responses={200: "Correo enviado", 404: "Usuario no encontrado"},
        tags=['Auth']

    )
    def post(self, request):
        """Genera un token de recuperación de contraseña y lo envía al correo del usuario."""
        email = request.data.get("email")
        response, status_code = self.auth_service.forgot_password(email)
        return Response(response, status=status_code)


class ResetPasswordView(APIView):
    auth_service = AuthService()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["token", "new_password"],
            properties={
                "token": openapi.Schema(type=openapi.TYPE_STRING, description="Token de recuperación recibido por correo"),
                "new_password": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Nueva contraseña")
            }
        ),
        responses={200: "Contraseña actualizada", 400: "Token inválido o expirado"},
        tags=['Auth']

    )
    def post(self, request):
        """Permite restablecer la contraseña con el token válido."""
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        response, status_code = self.auth_service.reset_password(token, new_password)
        return Response(response, status=status_code)