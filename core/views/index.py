# pylint: disable=missing-module-docstring
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
#from .. import serializers

class IndexView(APIView): # pylint: disable=missing-class-docstring
    permission_classes = [AllowAny]

    def get(self, request): # pylint: disable=missing-function-docstring,unused-argument
        return Response({'message': 'Hello, World!'}, status=status.HTTP_200_OK)
