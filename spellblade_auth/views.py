from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer, LoginRenewSerializer, LogoutSerializer, LogoutAllSerializer

class BaseView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = None

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(BaseView):
    serializer_class = LoginSerializer

class LoginRenewView(BaseView):
    serializer_class = LoginRenewSerializer

class LogoutView(BaseView):
    serializer_class = LogoutSerializer

class LogoutAllView(BaseView):
    serializer_class = LogoutAllSerializer
