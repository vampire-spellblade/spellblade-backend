class UpdatePersonalInfoView(APIView):
    '''View for updating user personal info'''
    serializer_class = UserChangePersonalInfoSerializer

    def get_serializer(self): # pylint: disable=missing-function-docstring
        return self.serializer_class()

    def put(self, request):
        '''PUT requests handling logic'''
        serializer = self.serializer_class(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateEmailView(APIView):
    '''View for updating user email'''
    serializer_class = UserChangeEmailSerializer

    def get_serializer(self): # pylint: disable=missing-function-docstring
        return self.serializer_class()

    def put(self, request):
        '''PUT requests handling logic'''
        serializer = self.serializer_class(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(APIView):
    '''View for updating user password'''
    serializer_class = UserChangePasswordSerializer

    def get_serializer(self): # pylint: disable=missing-function-docstring
        return self.serializer_class()

    def put(self, request):
        '''PUT requests handling logic'''
        serializer = self.serializer_class(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
