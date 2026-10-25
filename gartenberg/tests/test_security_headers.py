import os
import runpy
from unittest import mock

from django.test import TestCase, override_settings


@override_settings(
    # Die Login-Seite zieht die juntagrico-Assets über {% static %}; die ManifestStaticFilesStorage
    # aus den Projekt-Settings verlangt dafür ein zuvor erzeugtes collectstatic-Manifest.
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    },
)
class SecurityHeadersTest(TestCase):
    def test_login_page_sends_security_headers(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Frame-Options'], 'DENY')
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(response['Referrer-Policy'], 'same-origin')


class SecureCookieSettingsTest(TestCase):
    def load_settings(self, **env):
        with mock.patch.dict(os.environ, env):
            for key in ('JUNTAGRICO_DEBUG', 'JUNTAGRICO_HTTPS_ONLY'):
                if key not in env:
                    os.environ.pop(key, None)
            # frischer Namensraum, damit keine Werte eines früheren Imports übrig bleiben
            return runpy.run_module('gartenberg.settings')

    def test_secure_cookies_by_default(self):
        settings = self.load_settings()
        self.assertTrue(settings['SESSION_COOKIE_SECURE'])
        self.assertTrue(settings['CSRF_COOKIE_SECURE'])

    def test_no_secure_cookies_for_http_test_systems(self):
        settings = self.load_settings(JUNTAGRICO_HTTPS_ONLY='False')
        self.assertNotIn('SESSION_COOKIE_SECURE', settings)
        self.assertNotIn('CSRF_COOKIE_SECURE', settings)

    def test_no_secure_cookies_in_debug_mode(self):
        settings = self.load_settings(JUNTAGRICO_DEBUG='True')
        self.assertNotIn('SESSION_COOKIE_SECURE', settings)
