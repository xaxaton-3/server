import logging

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from rest_framework import status as status_code
from rest_framework.views import APIView
from rest_framework.response import Response

from notification.serializers import NotificationSerializer
from notification.models import Notification, INFO_STATUS


logger = logging.getLogger('__name__')


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
            return Response({'notification': new_notification.id})
        return Response(serializer.errors, status=status_code.HTTP_400_BAD_REQUEST)

    def send_email(self, email: str, message: str, status: int):
        mail_subject = 'Память Героям | У вас новое уведомление!'
        context = {'message': message, 'status': status}
        prepared_message = render_to_string('notification.html', context)
        email = EmailMessage(mail_subject, prepared_message, to=(email,))
        email.content_subtype = 'html'
        email.send()
        logger.debug(f'send email to {email}')


class UserNotifications(APIView):
    def get(self, request, user_id: int):
        not_received_notifications = Notification.objects.filter(to_user=user_id, received=False)
        notifications_to_show = [
            NotificationSerializer(notif).data
            for notif in not_received_notifications
        ]
        not_received_notifications.update(received=True)
        return Response(notifications_to_show)
