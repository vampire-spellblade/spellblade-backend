# pylint: disable=missing-module-docstring
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views.password_requirements import PasswordRequirements
from .views.signup import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/password-requirements/', PasswordRequirements.as_view(), \
        name='password_requirements'),

    # TODO: remove and replace with custom views
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/renew/', TokenRefreshView.as_view(), name='login/renew/'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
]
