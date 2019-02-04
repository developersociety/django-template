from django.test import TestCase
from django.utils import translation

class LanguageRedirectTest(TestCase):

    def tearDown():
        translation.deactivate()
    
    def test_english(self):
        response = self.client.get('/admin')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/en/admin/', fetch_redirect_response=False)
