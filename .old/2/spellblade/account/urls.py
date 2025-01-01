from django.urls import path

from .views import (
    IndexView,
)

urlpatterns = [
    path('hello-world/', IndexView.as_view()),
]
