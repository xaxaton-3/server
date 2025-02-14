from django.contrib.auth.models import User
from django.test import TestCase

from activity_journal.models import Journal


class JournalTest(TestCase):
    def test_logs_list(self):
        user = User.objects.create(email='test@mail.ru', username='user')
        journal1 = Journal.objects.create(user=user, log='1')
        journal2 = Journal.objects.create(user=user, log='2')
        journal3 = Journal.objects.create(user=user, log='3')
        response = self.client.get(f'/api/logs/list/{user.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['log'], journal1.log)
        self.assertEqual(response.data[1]['log'], journal2.log)
        self.assertEqual(response.data[2]['log'], journal3.log)

    def test_logs_list_user_not_exist(self):
        response = self.client.get('/api/logs/list/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_log_create(self):
        user = User.objects.create(email='test@mail.ru', username='user')
        logs_count_before = Journal.objects.count()
        response = self.client.post('/api/logs/create/', data={'user': user.id, 'log': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)
        logs_count_after = Journal.objects.count()
        self.assertNotEqual(logs_count_before, logs_count_after)
