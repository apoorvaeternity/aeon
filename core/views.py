from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from core.serializers import UserRegistrationSerializer, UserAuthenticationSerializer, UserLogoutSerializer, \
    ObjectiveCreateSerializer, ObjectiveListSerializer
from core.models import Objective


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
    authentication_classes = tuple()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            return Response({'token': serializer.validated_data['token']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    """
    Logout the user by deleting auth token
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data, context={'request': request})
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ObjectiveCreateView(APIView):
    """
    Create an objective
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ObjectiveCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ObjectiveListView(APIView):
    """
    View objectives of user
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ObjectiveListSerializer

    def post(self, request, *args, **kwargs):
        print(Objective.objects.filter(user=request.user))
        serializer = self.serializer_class(data=self.request.data, context={'request': request})
        if serializer.is_valid():
            queryset = Objective.objects.filter(user=request.user)
            serializer = self.serializer_class(queryset,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
