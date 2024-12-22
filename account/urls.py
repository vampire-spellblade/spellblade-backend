from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify, token_blacklist
from . import views

urlpatterns = [
    path('login/', token_obtain_pair, name='login'),
    path('login/renew/', token_refresh, name='login_renew'),
    path('login/verify/', token_verify, name='login_verify'),
    path('logout/', token_blacklist, name='logout'),
    path('signup/', views.signup, name='signup'),
]
