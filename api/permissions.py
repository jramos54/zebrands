from rest_framework import permissions

class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Permite acceso solo a administradores y superadministradores.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["admin", "super_admin"]

class IsAnonymousOrReadOnly(permissions.BasePermission):
    """
    Permite acceso de solo lectura a usuarios anónimos.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Permite GET para todos los usuarios
        return request.user.is_authenticated and request.user.role in ["admin", "super_admin"]
