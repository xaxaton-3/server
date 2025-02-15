import logging

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from rest_framework import status as status_code
from rest_framework.views import APIView
from rest_framework.response import Response

from notification.serializers import NotificationSerializer
from notification.models import Notification, INFO_STATUS


logger = logging.getLogger('__name__')


"""
@api {POST} /api/notification/create/ CreateNotification
@apiGroup Notification

@apiDescription Используется для отправки уведомления. Доступны два способа: отправка письма на почту и отправка внутренних уведомлений.

@apiBody {String} [email] Электронная почта пользователя (если указано - будет отправлено только письмо на почту)
@apiBody {String} message Сообщение, которое будет размещено в письме.
@apiBody {Number} status Определяет статус письма. Возможные варианты: 1 - уведомление об успехе, 2 - информационное сообщение, 3 - предупреждение, 4 - сообщение об ошибке, жалоба и т.п

@apiSuccess (Ответ) {Number} id Идентификатор рассмотренного запроса.

@apiSuccessExample Внутреннее уведомление отправлено:
    HTTP/1.1 200 OK
    {
        "id": 1
    }

@apiSuccessExample Уведомление отправлено на почту:
    HTTP/1.1 200 OK
    {
        "email": "red_hot_osu_pepper@mail.ru"
    }

@apiErrorExample {json} Пользователь не существует:
    HTTP/1.1 400 Bad requests
    {
        "to_user": [
            "Invalid pk \"500\" - object does not exist."
        ]
    }

@apiErrorExample {json} Обязательное поле пропущено:
    HTTP/1.1 400 Bad requests
    {
        "message": [
            "Обязательное поле."
        ]
    }
"""
class CreateNotification(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email:
            message = request.data.get('message', '')
            status = request.data.get('status', INFO_STATUS)
            self.send_email(email, message, status)
            return Response({'email': email})

        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            new_notification = serializer.save()
            return Response({'id': new_notification.id})
        return Response(serializer.errors, status=status_code.HTTP_400_BAD_REQUEST)

    def send_email(self, email: str, message: str, status: int):
        mail_subject = 'Память Героям | У вас новое уведомление!'
        context = {'message': message, 'status': status}
        prepared_message = render_to_string('notification.html', context)
        email = EmailMessage(mail_subject, prepared_message, to=(email,))
        email.content_subtype = 'html'
        email.send()
        logger.debug(f'send email to {email}')


"""
@api {GET} /api/notification/list/:id/ UserNotifications
@apiGroup Notification

@apiDescription Возвращает все внутренние уведомления, а также помечает их прочитанными пользователем.

@apiParam {Number} id Идентификатор пользователя, для которого необходимо получить уведомления.

@apiSuccess (Ответ) {Number} id Идентификатор уведомления.
@apiSuccess (Ответ) {Number} to_user Идентификатор получателя уведомления.
@apiSuccess (Ответ) {String} message Сообщение получателю.
@apiSuccess (Ответ) {Number} status Определяет статус письма. Возможные варианты: 1 - уведомление об успехе, 2 - информационное сообщение, 3 - предупреждение, 4 - сообщение об ошибке, жалоба и т.п.

@apiSuccessExample Список внутренних уведомлений:
    HTTP/1.1 200 OK
    [
        {
            "id": 1,
            "to_user": 1,
            "message": "Предоставленная вами информация прошла модерацию и была успешно опубликована! Спасибо!",
            "status": 1
        }
    ]
"""
class UserNotifications(APIView):
    def get(self, request, user_id: int):
        all_notifications = Notification.objects.filter(to_user=user_id)
        notifications_to_show = [
            NotificationSerializer(notif).data
            for notif in all_notifications
        ]
        all_notifications.update(received=True)
        return Response(notifications_to_show)
