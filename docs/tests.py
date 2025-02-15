from django.test import TestCase


class DocsTest(TestCase):
    def test_docs_available(self):
        response = self.client.get('/docs/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'docs.html')
