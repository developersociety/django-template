from django.test import TestCase
from django.utils import translation

class LanguageRedirectTest(TestCase):

    def tearDown(self):
        translation.deactivate()
    
    def test_english(self):
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/en/admin/', fetch_redirect_response=False)
    
    def test_dummy_translations(self):
        response = self.client.get('/admin', HTTP_ACCEPT_LANGUAGE='uni')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cy/', fetch_redirect_response=False)

