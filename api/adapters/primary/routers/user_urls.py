from django.urls import path
from api.adapters.primary.views.user_view import UserViewSet

user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path("users/", user_list, name="user-list"),
    path("users/<int:pk>/", user_detail, name="user-detail"),
    
]
