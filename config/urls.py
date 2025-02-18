
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

from api.adapters.primary.views.product_view import ProductViewSet
from api.adapters.primary.views.user_view import UserViewSet
from api.adapters.primary.views.log_view import LogViewSet
from api.adapters.primary.views.auth_view import LoginView, LogoutView, RefreshTokenView, ForgotPasswordView, ResetPasswordView


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Documentación de la API con Swagger",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
     url="http://127.0.0.1:8000"
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'users', UserViewSet, basename='users')
router.register(r'logs', LogViewSet, basename='logs')

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('api/', include(router.urls)),  
    # path('api/', include('api.adapters.primary.routers.auth_urls')),  
    path('api/login/', LoginView.as_view(), name="login"),
    path('api/logout/', LogoutView.as_view(), name="logout"),
    path('api/refresh/', RefreshTokenView.as_view(), name="refresh-token"),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('api/reset-password/', ResetPasswordView.as_view(), name="reset-password"),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)