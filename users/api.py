from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.decorators import with_authorization
from users.serializers import (
    UserSerializer, UserDetailSerializer,
    RegistrationSerializer, LoginSerializer
)
from users.utils import generate_token


class UserList(APIView):
    def get(self, request):
        users = [
            UserSerializer(user).data
            for user in User.objects.filter(is_active=True)
        ]
        return Response(users)


class UserDetail(APIView):
    def get(self, request, user_id: int):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'id': -1}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserDetailSerializer(user).data)


class Registration(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.initial_data.get('email'))
            if not user.check_password(serializer.initial_data.get('password')):
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response({'user': -1}, status=status.HTTP_404_NOT_FOUND)
        token = generate_token(user.id)
        return Response({'token': token, 'user': LoginSerializer(user).data})


class CheckToken(APIView):
    serializer_class = LoginSerializer

    @with_authorization
    def get(self, request):
        if not request.user:
            return Response({'id': -1}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(self.serializer_class(request.user).data)
