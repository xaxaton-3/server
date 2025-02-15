from mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from content.models import Defender


class ContentTest(TestCase):
    def setUp(self):
        self.form1 = Defender.objects.create(meta={'data': 1})
        self.form2 = Defender.objects.create(meta={'example': 'hello'})
        return super().setUp()


class RequestsListTest(ContentTest):
    def test_request_form_list_auth_not_admin(self):
        user = User.objects.create(email='user@mail.ru')
        user.set_password('123')
        user.save()
        response = self.client.post('/api/login/', data={'email': user.email, 'password': '123'})
        token = f'Bearer {response.data["token"]}'
        response = self.client.get('/api/content/forms/list/', headers={'Authorization': token})
        self.assertEqual(response.status_code, 403)

    def test_request_form_list_auth_admin(self):
        user = User.objects.create(email='admin@mail.ru', is_superuser=True)
        user.set_password('123')
        user.save()
        response = self.client.post('/api/login/', data={'email': user.email, 'password': '123'})
        token = f'Bearer {response.data["token"]}'
        response = self.client.get('/api/content/forms/list/', headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn('id', response.data[0])
        self.assertIn('meta', response.data[0])

    def test_request_form_list_no_auth(self):
        response = self.client.get('/api/content/forms/list/')
        self.assertEqual(response.status_code, 403)


class RequestsDeleteTest(ContentTest):
    def test_request_form_delete_auth_not_admin(self):
        user = User.objects.create(email='user@mail.ru')
        user.set_password('123')
        user.save()
        response = self.client.post('/api/login/', data={'email': user.email, 'password': '123'})
        token = f'Bearer {response.data["token"]}'
        response = self.client.post('/api/content/forms/delete/', data={'defender_id': self.form1.id}, headers={'Authorization': token})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['id'], -1)

    def test_request_form_delete_auth_admin(self):
        user = User.objects.create(email='admin@mail.ru', is_superuser=True)
        user.set_password('123')
        user.save()
        response = self.client.post('/api/login/', data={'email': user.email, 'password': '123'})
        token = f'Bearer {response.data["token"]}'
        response = self.client.post('/api/content/forms/delete/', data={'defender_id': self.form1.id}, headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['id'], self.form1.id)

    def test_request_form_delete_no_auth(self):
        response = self.client.post('/api/content/forms/delete/', data={'defender_id': self.form1.id})
        self.assertEqual(response.data['id'], -1)
        self.assertEqual(response.status_code, 403)


class RequestsCreateTest(TestCase):
    def test_create_form(self):
        count_before = Defender.objects.count()
        response = self.client.post('/api/content/forms/create/', data={'meta': '{"number": 1}'})
        count_after = Defender.objects.count()
        self.assertIn('id',response.data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(count_before, count_after)
