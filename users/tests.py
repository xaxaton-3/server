from django.contrib.auth.models import User
from django.test import TestCase


class UsersTest(TestCase):
    def test_users_list(self):
        user1 = User.objects.create(email='test@mail.ru', username='user')
        user2 = User.objects.create(email='example@yandex.com', username='example')
        response = self.client.get('/api/users/list/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['email'], user1.email)
        self.assertEqual(response.data[1]['email'], user2.email)

    def test_user_detail_success(self):
        user = User.objects.create(email='test@mail.ru', username='user')
        response = self.client.get(f'/api/user/detail/{user.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)
        self.assertNotEqual(response.data['id'], -1)

    def test_user_detail_bad(self):
        response = self.client.get('/api/user/detail/1/')
        self.assertEqual(response.status_code, 404)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['id'], -1)
