# pylint: disable=missing-module-docstring
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class IndexView(APIView):
    '''Sends a simple message and can be used for health checks.'''
    permission_classes = (AllowAny,) # Unprotected endpoint

    def get(self, request): # pylint: disable=missing-function-docstring,unused-argument
        return Response({'message': 'Hello, World!'}, status=status.HTTP_200_OK)
