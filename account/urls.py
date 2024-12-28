# pylint: disable=missing-module-docstring

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from .views import (
    SignUpView
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/renew/', TokenRefreshView.as_view(), name='login_renew'),
    path('login/verify/', TokenVerifyView.as_view(), name='login_verify'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
