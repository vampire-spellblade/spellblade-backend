# pylint: disable=missing-module-docstring

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from .views import (
    SignUpView,
    UpdatePersonalInfoView,
    UpdateEmailView,
    UpdatePasswordView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/renew/', TokenRefreshView.as_view(), name='login_renew'),
    path('login/verify/', TokenVerifyView.as_view(), name='login_verify'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('update/personal-info/', UpdatePersonalInfoView.as_view(), name='update_personal_info'),
    path('update/email/', UpdateEmailView.as_view(), name='update_email'),
    path('update/password/', UpdatePasswordView.as_view(), name='update_password'),
]
