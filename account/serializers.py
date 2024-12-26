# pylint: disable=missing-module-docstring

from django.contrib.auth import get_user_model
from rest_framework import serializers # pylint: disable=unused-import
#from .models import ()

User = get_user_model()
