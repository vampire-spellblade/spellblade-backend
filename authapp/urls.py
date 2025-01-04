from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views.password_requirements import PasswordRequirementsView
from .views.signup import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/password-requirements/', PasswordRequirementsView.as_view(), name='signup_password_requirements'),

    # TODO: Remove and replace with custom views. (Priority: High)
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/renew/', TokenRefreshView.as_view(), name='login/renew/'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
]
