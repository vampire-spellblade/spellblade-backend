from django.urls import path
from .views import LoginView, LoginRenewView, LogoutView, LogoutAllView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/renew/', LoginRenewView.as_view(), name='login_renew'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/all/', LogoutAllView.as_view(), name='logout_all'),
]
