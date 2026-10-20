from axes.models import AccessAttempt
from django.test import RequestFactory, TestCase, override_settings
from juntagrico.entity.member import Member

from gartenberg.auth import client_ip


class ClientIpTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_without_proxy_uses_remote_addr(self):
        request = self.factory.get('/', REMOTE_ADDR='192.0.2.1')
        self.assertEqual(client_ip(request), '192.0.2.1')

    def test_uses_address_appended_by_proxy(self):
        request = self.factory.get('/', REMOTE_ADDR='10.0.0.1', HTTP_X_FORWARDED_FOR='203.0.113.7')
        self.assertEqual(client_ip(request), '203.0.113.7')

    def test_ignores_spoofed_entries_sent_by_client(self):
        request = self.factory.get('/', REMOTE_ADDR='10.0.0.1',
                                   HTTP_X_FORWARDED_FOR='198.51.100.99, 203.0.113.7')
        self.assertEqual(client_ip(request), '203.0.113.7')


@override_settings(
    # Login- und Sperrseite ziehen die juntagrico-Assets über {% static %}; die ManifestStaticFilesStorage
    # aus den Projekt-Settings verlangt dafür ein zuvor erzeugtes collectstatic-Manifest.
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    },
)
class LoginLockoutTest(TestCase):
    password = 'richtiges-passwort'

    def setUp(self):
        member = Member.objects.create(
            first_name='Anna', last_name='Muster', email='anna@example.com',
            addr_street='Teststrasse 1', addr_zipcode='5000', addr_location='Aarau',
            phone='079 000 00 00', reachable_by_email=False,
        )
        # juntagrico setzt confirmed beim Anlegen zurück, das Login verlangt aber eine bestätigte Adresse
        Member.objects.filter(pk=member.pk).update(confirmed=True)
        member.user.set_password(self.password)
        member.user.save()

    def login(self, password, ip='203.0.113.7'):
        return self.client.post('/accounts/login/', {'username': 'anna@example.com', 'password': password},
                                HTTP_X_FORWARDED_FOR=ip)

    def test_locks_ip_after_five_failures(self):
        for _ in range(4):
            self.assertEqual(self.login('falsch').status_code, 200)
        response = self.login('falsch')
        self.assertEqual(response.status_code, 429)
        self.assertContains(response, 'Zu viele fehlgeschlagene Anmeldeversuche', status_code=429)
        self.assertContains(response, '30 Minuten', status_code=429)
        # auch das richtige Passwort wird während der Sperre abgewiesen
        self.assertEqual(self.login(self.password).status_code, 429)

    def test_spoofed_forwarded_for_does_not_bypass_lockout(self):
        for i in range(5):
            self.login('falsch', ip=f'198.51.100.{i}, 203.0.113.7')
        self.assertEqual(self.login(self.password, ip='198.51.100.50, 203.0.113.7').status_code, 429)

    def test_other_ip_is_not_locked(self):
        for _ in range(5):
            self.login('falsch')
        self.assertEqual(self.login(self.password, ip='203.0.113.8').status_code, 302)

    def test_successful_login_resets_failures(self):
        for _ in range(4):
            self.login('falsch')
        self.assertEqual(self.login(self.password).status_code, 302)
        self.assertFalse(AccessAttempt.objects.exists())
