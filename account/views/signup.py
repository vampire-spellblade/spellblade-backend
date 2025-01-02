from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..serializers import UserCreationSerializer

class SignUpView(APIView): # pylint: disable=missing-class-docstring
    permission_classes = [AllowAny]
    serializer_class = UserCreationSerializer

    def get_serializer(self): # pylint: disable=missing-function-docstring
        return self.serializer_class()

    def post(self, request): # pylint: disable=missing-function-docstring
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
