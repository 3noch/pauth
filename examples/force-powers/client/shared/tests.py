from django.conf import settings
from django.test import TestCase

from utils import get_all_scopes


class GetAllScopesTest(TestCase):
    def setUp(self):
        self.original = settings.AUTHORIZATION_HOST

    def tearDown(self):
        settings.AUTHORIZATION_HOST = self.original

    def test_valid_url(self):
        scopes = get_all_scopes()
        self.assertIsNotNone(scopes)
        self.assertTrue(len(scopes) > 0)

    def test_invalid_url(self):
        settings.AUTHORIZATION_HOST = 'notalive:8000'
        self.assertIsNone(get_all_scopes())
