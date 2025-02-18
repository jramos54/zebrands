from django.urls import path
from api.adapters.primary.views.product_view import ProductViewSet

urlpatterns = [
    path('', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='products_list'),
    path('<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='products_detail'),
]
