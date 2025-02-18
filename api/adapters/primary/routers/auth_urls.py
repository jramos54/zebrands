from django.urls import path
from rest_framework.routers import DefaultRouter
from api.adapters.primary.views.auth_view import LoginView, LogoutView, RefreshTokenView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('refresh/', RefreshTokenView.as_view(), name="refresh-token"),
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('reset-password/', ResetPasswordView.as_view(), name="reset-password"),
]