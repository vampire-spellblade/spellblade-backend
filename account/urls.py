from django.urls import path
from rest_framework_simplejwt.views import token_refresh_sliding, token_refresh, token_verify, token_obtain_pair, token_obtain_sliding, token_blacklist
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
