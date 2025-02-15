from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from activity_journal.serializers import UserLogSerializer
from activity_journal.models import Journal


"""
@api {GET} /api/logs/list/:id/ UserLogs
@apiGroup Logs

@apiDescription Получение действий пользователя. Доступно только администратору системы.

@apiParam {Number} id Идентификатор пользователя, для которого необходимо получить логи.

@apiSuccess (Ответ) {Object[]} journal Журнал действий пользователя.
@apiSuccess (Ответ) {Number} journal.id Идентификатор лога.
@apiSuccess (Ответ) {String} journal.log Запись лога.
@apiSuccess (Ответ) {Date} journal.datetime Дата записи лога.
@apiSuccess (Ответ) {Number} journal.user Идентификатор пользователя, чье действие записывается в лог.

@apiSuccessExample Список действий пользователя:
    HTTP/1.1 200 OK
    [
        {
            "id": 1,
            "log": "sent request to create person",
            "datetime": "2025-02-15T12:35:39.850569Z",
            "user": 1
        }
    ]
"""
class UserLogs(APIView):
    def get(self, request, user_id: int):
        logs = [
            UserLogSerializer(log).data
            for log in Journal.objects.filter(user=user_id)
        ]
        return Response(logs)


"""
@api {POST} /api/logs/create/ UserLogsCreate
@apiGroup Logs

@apiDescription Запись действия в лог.

@apiBody {Number} user Идентификатор пользователя, для которого необходимо записать в лог.
@apiBody {String} log Текст записи.

@apiSuccess (Ответ) {Number} id Идентификатор созданного лога.

@apiSuccessExample Запись в журнале создана:
    HTTP/1.1 200 OK
    {
        "id": 1
    }
"""
class UserLogsCreate(APIView):
    def post(self, request):
        serializer = UserLogSerializer(data=request.data)
        if serializer.is_valid():
            new_log = serializer.save()
            return Response({'id': new_log.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
