from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from content.serializers import DefenderFormSerializer, DefenderFormDeleteSerializer
from content.models import Defender
from users.decorators import with_authorization


"""
@api {POST} /api/content/forms/create/ PersonRequestCreate
@apiGroup Content

@apiDescription Используется для сохранения формы с любым набором полей для возможности отправки запроса в интеграцию
после одобрения формы администратором.

@apiBody {String} meta Набор полей и соответствующих им значений в формате JSON, полученный после заполнения формы пользователем.

@apiSuccess (Ответ) {Number} id Идентификатор пользователя.

@apiSuccessExample Форма создана:
    HTTP/1.1 200 OK
    {
        "id": 1
    }
"""
class PersonRequestCreate(APIView):
    serializer_class = DefenderFormSerializer

    def post(self, request):
        serializer = DefenderFormSerializer(data=request.data)
        if serializer.is_valid():
            new_request = serializer.save()
            return Response({'id': new_request.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
@api {POST} /api/content/forms/delete/ PersonRequestDelete
@apiGroup Content

@apiDescription Используется после рассмотрения запроса администратором для скрытия запроса из списка нерассмотренных.

@apiBody {Number} defender_id Идентификатор запроса, необходимого убрать из перечня нерассмотренных.

@apiSuccess (Ответ) {Number} id Идентификатор рассмотренного запроса.

@apiSuccessExample Запрос отработан:
    HTTP/1.1 200 OK
    {
        "id": 1
    }

@apiErrorExample {json} Пользователь не авторизован как администратор:
    HTTP/1.1 403 Forbidden
    {
        "id": -1
    }
"""
class PersonRequestDelete(APIView):
    serializer_class = DefenderFormDeleteSerializer

    @with_authorization
    def post(self, request):
        defender_id = -1
        if request.user and request.user.is_superuser:
            defender_id = int(request.data.get('defender_id', -1))
            Defender.objects.filter(id=defender_id).delete()
            return Response({'id': defender_id})
        return Response({'id': defender_id}, status=status.HTTP_403_FORBIDDEN)


"""
@api {GET} /api/content/forms/list/ PersonRequestList
@apiGroup Content

@apiDescription Список нерассмотренных форм для администратора.

@apiSuccess (Ответ) {Object[]} forms Нерассмотренные формы.
@apiSuccess (Ответ) {Number} forms.id Идентификатор формы.
@apiSuccess (Ответ) {Json} forms.meta Содержимое формы в формате JSON.

@apiSuccessExample Список форм на рассмотрении у администратора:
    HTTP/1.1 200 OK
    [
        {
            "id": 1,
            "meta": {
                "name": "Александр",
                "surname": "Матросов"
            }
        }
    ]

@apiErrorExample {json} Пользователь не авторизован как администратор:
    HTTP/1.1 403 Forbidden
    {}
"""
class PersonRequestsList(APIView):
    serializer_class = DefenderFormSerializer

    @with_authorization
    def get(self, request):
        if request.user and request.user.is_superuser:
            forms = [self.serializer_class(form).data for form in Defender.objects.filter(is_open=True)]
            return Response(forms)
        return Response({}, status=status.HTTP_403_FORBIDDEN)
