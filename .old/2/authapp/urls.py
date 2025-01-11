from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views.signup import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),

    # TODO: Remove and replace with custom views. (Priority: High)
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/renew/', TokenRefreshView.as_view(), name='login/renew/'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
]
