from rest_framework import viewsets, status
from rest_framework.response import Response
from api.adapters.primary.serializers.user_serializer import UserSerializer
from api.application.user_service import UserService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permissions import IsAdminOrSuperAdmin
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ViewSet):
    """Vista para gestionar usuarios."""
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.user_service = UserService()

    @swagger_auto_schema(
        responses={200: UserSerializer(many=True)},
        tags=['Users']
    )
    def list(self, request):
        """Lista usuarios con filtros opcionales."""
        filters = request.query_params.dict()
        users = self.user_service.list_users(filters)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID del usuario", type=openapi.TYPE_INTEGER)
        ],
        responses={200: UserSerializer(), 404: "Usuario no encontrado"},
        tags=['Users']
    )
    def retrieve(self, request, pk=None):
        """Obtiene un usuario por ID."""
        user = self.user_service.get_user(int(pk))
        if not user:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer(), 400: "Datos inválidos"},
        tags=['Users']
    )
    def create(self, request):
        """Crea un nuevo usuario."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
