from django.db import models
from django.contrib.auth.models import AbstractUser
from api.models import User
   
class ProductModel(models.Model):
    """Modelo de Producto."""
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    stock = models.IntegerField()
    short_description = models.TextField()
    long_description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

class LogModel(models.Model):
    """Modelo de Log para auditoría de cambios."""
    admin = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="logs"
    )
    target_id = models.IntegerField()
    action = models.CharField(max_length=50)
    changes = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        admin_name = self.admin.username if self.admin else "Desconocido"
        return f"Log {self.id}: {self.action} por {admin_name} en {self.target_id}"

class ProductQuery(models.Model):
    product_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    query_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("product_id", "user")  

    def __str__(self):
        return f"Producto {self.product_id} consultado {self.query_count} veces por usuario {self.user.id}"