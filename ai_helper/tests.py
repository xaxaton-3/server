from mock import patch

from django.test import TestCase, override_settings

from ai_helper.ai_client import AiClient


def mock_ai_response(self, text: str) -> str:
    return 'some text'


@override_settings(MISTRAL_TOKEN='token')
@patch('ai_helper.ai_client.AiClient.send_request', mock_ai_response)
class AiClientTest(TestCase):
    def test_ai_client(self):
        client = AiClient()
        self.assertEqual(client.get_beautiful_text(''), 'some text')


@override_settings(MISTRAL_TOKEN='token')
@patch('ai_helper.ai_client.AiClient.send_request', mock_ai_response)
class AiApiTest(TestCase):
    def test_get_formated_text(self):
        response = self.client.post('/api/unsafe/airefactor/text/', data={'text': 'my bad text here'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.data)
        self.assertEqual(response.data['text'], 'some text')

    def test_get_formated_text_bad_param(self):
        response = self.client.post('/api/unsafe/airefactor/text/', data={'not_text': 'really bad value'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('text', response.data)
