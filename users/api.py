from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from users.serializers import UserSerializer, UserDetailSerializer


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
            return Response({'id': -1})
        return Response(UserDetailSerializer(user).data)
