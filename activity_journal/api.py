from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from activity_journal.serializers import UserLogSerializer
from activity_journal.models import Journal


class UserLogs(APIView):
    def get(self, request, user_id: int):
        logs = [
            UserLogSerializer(log).data
            for log in Journal.objects.filter(user=user_id)
        ]
        return Response(logs)


class UserLogsCreate(APIView):
    def post(self, request):
        serializer = UserLogSerializer(data=request.data)
        if serializer.is_valid():
            new_log = serializer.save()
            return Response({'id': new_log.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
