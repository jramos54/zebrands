from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.adapters.primary.serializers.product_serializer import ProductSerializer
from api.application.product_service import ProductService
from api.application.log_service import LogService
from api.application.user_service import UserService
from api.adapters.secondary.services.email_service import NotificationService
from api.adapters.secondary.services.email_service import EmailService
from api.domain.entities.product import Product
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.permissions import IsAdminOrSuperAdmin, IsAnonymousOrReadOnly
from django.db.utils import IntegrityError
from api.models import User



class ProductViewSet(viewsets.ViewSet):
    """Vista para gestionar productos."""
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]
    
    product_service = ProductService()
    log_service = LogService()
    user_service = UserService()
    notification_service = EmailService()
    
    def get_permissions(self):
        """Asigna permisos basados en la acción."""
        if self.action in ["list", "retrieve"]:
            return [IsAnonymousOrReadOnly()]
        return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Filtrar por categoría", type=openapi.TYPE_STRING),
            openapi.Parameter('brand', openapi.IN_QUERY, description="Filtrar por marca", type=openapi.TYPE_STRING),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Filtrar por precio mínimo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Filtrar por precio máximo", type=openapi.TYPE_NUMBER),
        ],
        responses={200: ProductSerializer(many=True)},
        tags=['Products']
    )
    def list(self, request):
        """Lista productos con filtros opcionales."""
        filters = request.query_params.dict()
        products = self.product_service.list_products(filters)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID del producto", type=openapi.TYPE_INTEGER)
        ],
        responses={200: ProductSerializer(), 404: "Producto no encontrado"},
        tags=['Products']
    )
    def retrieve(self, request, pk=None):
        """Obtiene un producto por ID y registra la consulta si el usuario tiene el rol 'anonymous'."""
        try:
            product = self.product_service.get_product(int(pk))
        except ObjectDoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        print(f"Usuario: {request.user.id}, Rol: {request.user.role}") 
        if request.user.role == "anonymus":
            print("Usuario es anónimo, registrando consulta...")  
            self.product_service.increment_query_count(product.id, request.user)

        serializer = ProductSerializer(product)
        return Response(serializer.data)
   
    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={201: ProductSerializer(), 400: "Datos inválidos"},
        tags=['Products']
    )
    def create(self, request):
        """Crea un nuevo producto y maneja duplicados."""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = serializer.save()
                
                self.log_service.log_product_action(product.id, request.user.id, "created")

                admin_emails = self.user_service.get_admin_emails()
                for email in admin_emails:
                    self.notification_service.send_email(
                        to_email=email,
                        subject="Nuevo Producto Creado",
                        message=f"El producto {product.name} ha sido creado por {request.user.username}."
                    )

                return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            except IntegrityError:
                return Response({"error": "Ya existe un producto con este SKU u otro campo único."}, 
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID del producto", type=openapi.TYPE_INTEGER)
        ],
        request_body=ProductSerializer,
        responses={200: ProductSerializer(), 400: "Datos inválidos", 404: "Producto no encontrado"},
        tags=['Products']
    )
    def update(self, request, pk=None):
        """Actualiza completamente un producto (PUT)."""
        try:
            product = self.product_service.get_product(int(pk))
        except ObjectDoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            try:
                product = serializer.save()

                self.log_service.log_product_action(product.id, request.user.id, "updated")

                admin_emails = self.user_service.get_admin_emails()
                for email in admin_emails:
                    self.notification_service.send_email(
                        to_email=email,
                        subject="Producto Actualizado",
                        message=f"El producto {product.name} ha sido actualizado por {request.user.username}."
                    )

                return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

            except ValueError as e:  
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['is_active'],
            properties={
                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="True para activar, False para desactivar")
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de confirmación")
                }
            ),
            404: "Producto no encontrado"
        },
        tags=['Products']
    )
    @action(detail=True, methods=["patch"])
    def toggle_active(self, request, pk=None):
        """Activa o desactiva un producto."""
        try:
            product = self.product_service.get_product(int(pk))  
        except ObjectDoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        product.is_active = not product.is_active  

        try:
            updated_product = self.product_service.update_product(product, {})  
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        action_type = "activated" if updated_product.is_active else "deactivated"
        self.log_service.log_product_action(updated_product.id, request.user.id, action_type)

        admin_emails = self.user_service.get_admin_emails()
        for email in admin_emails:
            self.notification_service.send_email(
                to_email=email,
                subject="Estado de Producto Modificado",
                message=f"El producto {updated_product.name} ha sido {'activado' if updated_product.is_active else 'desactivado'} por {request.user.username}."
            )

        return Response(
            {"message": f"Producto {'activado' if updated_product.is_active else 'desactivado'}"},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['stock'],
            properties={
                'stock': openapi.Schema(type=openapi.TYPE_INTEGER, description="Cantidad de stock a actualizar")
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de confirmación")
                }
            ),
            404: "Producto no encontrado"
        },
        tags=['Products']
    )
    @action(detail=True, methods=["patch"])
    def update_stock(self, request, pk=None):
        """Modifica el stock de un producto."""
        try:
            product = self.product_service.get_product(int(pk))
        except ObjectDoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        new_stock = request.data.get("stock")

        if new_stock is None or not isinstance(new_stock, int) or new_stock < 0:
            return Response({"error": "El stock debe ser un número entero positivo"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_product = self.product_service.update_product(product, {"stock": new_stock})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        self.log_service.log_product_action(updated_product.id, request.user.id, "stock_updated")

        admin_emails = self.user_service.get_admin_emails()
        for email in admin_emails:
            self.notification_service.send_email(
                to_email=email,
                subject="Stock de Producto Modificado",
                message=f"El stock del producto {updated_product.name} ha sido actualizado a {new_stock} por {request.user.username}."
            )

        return Response(
            {"message": f"Stock actualizado a {updated_product.stock}"},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['price'],
            properties={
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Nuevo precio del producto")
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de confirmación")
                }
            ),
            404: "Producto no encontrado"
        },
        tags=['Products']
    )
    @action(detail=True, methods=["patch"])
    def update_price(self, request, pk=None):
        """Modifica el precio de un producto."""
        try:
            product = self.product_service.get_product(int(pk))
        except ObjectDoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        new_price = request.data.get("price")

        if new_price is None or not isinstance(new_price, (int, float)) or new_price <= 0:
            return Response({"error": "El precio debe ser un número positivo"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_product = self.product_service.update_product(product, {"price": new_price})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        self.log_service.log_product_action(updated_product.id, request.user.id, "price_updated")

        admin_emails = self.user_service.get_admin_emails()
        for email in admin_emails:
            self.notification_service.send_email(
                to_email=email,
                subject="Precio de Producto Modificado",
                message=f"El precio del producto {updated_product.name} ha sido actualizado a ${new_price} por {request.user.username}."
            )

        return Response(
            {"message": f"Precio actualizado a ${updated_product.price}"},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID del producto", type=openapi.TYPE_INTEGER)
        ],
        responses={204: "Producto eliminado", 404: "Producto no encontrado"},
        tags=['Products']
    )
    def destroy(self, request, pk=None):
        """Elimina un producto (DELETE)."""
        try:
            product = self.product_service.get_product(int(pk))
        except ObjectDoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        self.product_service.delete_product(product.id)

        self.log_service.log_product_action(product.id, request.user.id, "deleted")

        admin_emails = self.user_service.get_admin_emails()
        for email in admin_emails:
            self.notification_service.send_email(
                to_email=email,
                subject="Producto Eliminado",
                message=f"El producto {product.name} ha sido eliminado por {request.user.username}."
            )

        return Response({"message": "Producto eliminado"}, status=status.HTTP_204_NO_CONTENT)

