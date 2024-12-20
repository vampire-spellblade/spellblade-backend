from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('login/renew/', views.login_renew, name='login_renew'),
    path('signup/', views.signup, name='signup'),
]
