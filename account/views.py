from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UpdateUserPersonalInfoSerializer, UpdateUserEmailSerializer, UpdateUserPasswordSerializer

@api_view(['POST'])
@permission_classes([])
def signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_user_info(request, serializer_class):
    user = request.user
    serializer = serializer_class(user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_personal_info(request):
    return update_user_info(request, UpdateUserPersonalInfoSerializer)

@api_view(['POST'])
def update_email(request):
    return update_user_info(request, UpdateUserEmailSerializer)

@api_view(['POST'])
def update_password(request):
    return update_user_info(request, UpdateUserPasswordSerializer)
