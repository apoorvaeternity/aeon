from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from core.serializers import UserRegistrationSerializer, UserAuthenticationSerializer


class UserRegistrationView(APIView):
    """
    Register a user
    """

    serializer_class = UserRegistrationSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuthenticationView(APIView):
    """
    Retrieve auth token for a user
    """
    serializer_class = UserAuthenticationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            return Response({'token': serializer.validated_data['token']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
