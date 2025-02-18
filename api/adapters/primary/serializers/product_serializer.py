from rest_framework import serializers
from api.domain.entities.product import Product
from api.application.product_service import ProductService  
from django.utils.timezone import now  

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    sku = serializers.CharField()
    price = serializers.FloatField()
    brand = serializers.CharField()
    category = serializers.CharField()
    stock = serializers.IntegerField()
    short_description = serializers.CharField()
    long_description = serializers.CharField()
    is_active = serializers.BooleanField(default=True)
    
    def create(self, validated_data):
        """Usa el servicio de productos para crear y persistir el producto."""
        product_service = ProductService()  

        validated_data["created_at"] = now()
        validated_data["updated_at"] = now()
        
        return product_service.create_product(validated_data) 
    
    def update(self, instance, validated_data):
        """Actualiza un producto existente."""
        product_service = ProductService()
        return product_service.update_product(instance, validated_data) 
