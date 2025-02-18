from django.urls import path
from api.adapters.primary.views.log_view import LogViewSet

log_list = LogViewSet.as_view({"get": "list"})
log_detail = LogViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("logs/", log_list, name="logs_list"),
    path("logs/<int:pk>/", log_detail, name="logs_detail"),
    path("anonymous-queries/", LogViewSet.as_view({"get": "list_anonymous_queries"})),
]
