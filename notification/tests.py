from mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from notification.models import Notification


def check_email_content(email):
    assert email.content_subtype == 'html'
    assert len(email.subject) > 0
    assert len(email.body) > 0


class NotificationTest(TestCase):
    def test_notification_list(self):
        user = User.objects.create(email='test@mail.ru', username='user')
        notification1 = Notification.objects.create(to_user=user, message='example1', status=1, received=True)
        notification2 = Notification.objects.create(to_user=user, message='example2', status=2, received=False)
        notification3 = Notification.objects.create(to_user=user, message='example3', status=3, received=False)
        response = self.client.get(f'/api/notification/list/{user.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['message'], notification1.message)
        self.assertEqual(response.data[0]['status'], notification1.status)
        self.assertEqual(response.data[0]['received'], notification1.received)
        self.assertEqual(response.data[1]['message'], notification2.message)
        self.assertEqual(response.data[1]['status'], notification2.status)
        self.assertEqual(response.data[1]['received'], notification2.received)
        self.assertEqual(response.data[2]['message'], notification3.message)
        self.assertEqual(response.data[2]['status'], notification3.status)
        self.assertEqual(response.data[2]['received'], notification3.received)
        notification1 = Notification.objects.get(id=notification1.id)
        notification2 = Notification.objects.get(id=notification2.id)
        notification3 = Notification.objects.get(id=notification3.id)
        self.assertEqual(notification1.received, True)
        self.assertEqual(notification2.received, True)
        self.assertEqual(notification3.received, True)
        response = self.client.get(f'/api/notification/list/{user.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['received'], True)
        self.assertEqual(response.data[1]['received'], True)
        self.assertEqual(response.data[2]['received'], True)

    def test_notification_list_user_not_exist(self):
        response = self.client.get('/api/notification/list/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_internal_notification_create(self):
        user = User.objects.create(email='test@mail.ru', username='user')
        notifications_count_before = Notification.objects.count()
        response = self.client.post('/api/notification/create/', data={'to_user': user.id, 'message': 'test', 'status': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)
        notifications_count_after = Notification.objects.count()
        self.assertNotEqual(notifications_count_before, notifications_count_after)

    @patch('django.core.mail.EmailMessage.send', check_email_content)
    def test_email_notification_create(self):
        response = self.client.post('/api/notification/create/', data={'email': 'test@mail.ru', 'message': 'test', 'status': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], 'test@mail.ru')
