from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from . import serializers

@api_view(['POST'])
def get_user(request):
    return Response({
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([])
def signup(request):
    serializer = serializers.UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({}, status=status.HTTP_200_OK)

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
    return update_user_info(request, serializers.UserPersonalInfoSerializer)

@api_view(['POST'])
def update_email(request):
    return update_user_info(request, serializers.UserEmailSerializer)

@api_view(['POST'])
def update_password(request):
    return update_user_info(request, serializers.UserPasswordSerializer)
