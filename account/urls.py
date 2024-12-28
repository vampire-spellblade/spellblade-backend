# pylint: disable=missing-module-docstring

from django.urls import path
from .views import (
    LoginView,
    LoginRenewView,
    LoginVerifyView,
    LogoutView,
    SignUpView,
    UpdatePersonalInfoView,
    UpdateEmailView,
    UpdatePasswordView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/renew/', LoginRenewView.as_view(), name='login_renew'),
    path('login/verify/', LoginVerifyView.as_view(), name='login_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('update/personal-info/', UpdatePersonalInfoView.as_view(), name='update_personal_info'),
    path('update/email/', UpdateEmailView.as_view(), name='update_email'),
    path('update/password/', UpdatePasswordView.as_view(), name='update_password'),
]
