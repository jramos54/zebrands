from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    """Modelo de usuario personalizado."""
    ROLES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('anonymous', 'Anonymous'),
    )

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=ROLES, default='anonymous')
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_users')
    token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups", 
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  
        blank=True
    )

    def __str__(self):
        return self.username