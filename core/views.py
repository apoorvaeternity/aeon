from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from core.serializers import UserRegistrationSerializer


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
