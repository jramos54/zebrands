from rest_framework import serializers
from api.domain.entities.user import User
from api.application.user_service import UserService  
import datetime

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    is_active = serializers.BooleanField()
    created_by = serializers.IntegerField(required=False, allow_null=True)
    updated_by = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data):
        """Convierte el diccionario a un objeto `User` y lo envía al servicio para persistencia."""
        user_service = UserService()

        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],  # Se encripta en el servicio
            role=validated_data["role"],
            is_active=validated_data["is_active"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            created_by=validated_data.get("created_by"),  
            updated_by=validated_data.get("updated_by"),  
        )
        return user_service.create_user(user)  