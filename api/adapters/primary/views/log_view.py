from rest_framework import viewsets, status
from rest_framework.response import Response
from api.adapters.primary.serializers.log_serializer import LogSerializer
from api.application.log_service import LogService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permissions import IsAdminOrSuperAdmin
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action


class LogViewSet(viewsets.ViewSet):
    """Vista para gestionar los registros de auditoría."""
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.log_service = LogService()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description="Filtrar logs por ID de usuario", type=openapi.TYPE_INTEGER),
            openapi.Parameter('product_id', openapi.IN_QUERY, description="Filtrar logs por ID de producto", type=openapi.TYPE_INTEGER),
            openapi.Parameter('action', openapi.IN_QUERY, description="Filtrar logs por tipo de acción", type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Fecha de inicio para filtro de logs (YYYY-MM-DD)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Fecha de fin para filtro de logs (YYYY-MM-DD)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ],
        responses={200: LogSerializer(many=True)},
        tags=['Logs']
    )
    def list(self, request):
        """Lista registros de auditoría con filtros opcionales."""
        filters = request.query_params.dict()
        logs = self.log_service.list_logs(filters)

        if not logs:
            return Response({"message": "No hay registros disponibles."}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={
            200: LogSerializer(),
            404: "Log no encontrado"
        },
        tags=['Logs']
    )
    def retrieve(self, request, pk=None):
        """Obtiene el detalle de un log por su ID."""
        try:
            log = self.log_service.get_log(int(pk))
            serializer = LogSerializer(log)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Log no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=["get"], url_path="anonymous-queries")
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "product_id",
                openapi.IN_QUERY,
                description="ID del producto a consultar (opcional)",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: "Lista de productos consultados por usuarios anónimos"},
        tags=['Logs']
    )
    def list_anonymous_queries(self, request):
        """Obtiene las consultas de productos realizadas por usuarios anónimos."""
        product_id = request.query_params.get("product_id")
        queries = self.log_service.get_anonymous_queries(product_id)

        if not queries:
            return Response({"message": "No hay registros disponibles."}, status=status.HTTP_204_NO_CONTENT)

        return Response(queries, status=status.HTTP_200_OK)
