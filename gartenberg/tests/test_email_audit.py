from django.test import RequestFactory, TestCase

from gartenberg.middleware import EmailAuditMiddleware
from gartenberg.models import EmailAuditLog


class EmailAuditMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = EmailAuditMiddleware(get_response=lambda r: None)

    def test_erstellt_log_bei_mail_versand(self):
        request = self.factory.post('/email/write/', {
            'submit': 'Senden',
            'from_email': 'laura@gartenberg.ch',
            'subject': 'Ernte-Info KW 17',
            'to_list': 'all_subscriptions',
        })
        self.middleware(request)
        self.assertEqual(EmailAuditLog.objects.count(), 1)
        log = EmailAuditLog.objects.get()
        self.assertEqual(log.sender, 'laura@gartenberg.ch')
        self.assertEqual(log.subject, 'Ernte-Info KW 17')
        self.assertIn('Abo-BezieherInnen', log.recipient_groups)
        self.assertEqual(log.url, '/email/write/')

    def test_alle_empfaenger_gruppen(self):
        request = self.factory.post('/email/write/', {
            'submit': 'Senden',
            'from_email': 'info@gartenberg.ch',
            'subject': 'Test',
            'to_list': ['all_subscriptions', 'all_shares'],
            'to_members': ['1'],
            'to_areas': ['2'],
            'to_jobs': ['3'],
            'to_depots': ['4'],
            'copy': 'on',
        })
        self.middleware(request)
        log = EmailAuditLog.objects.get()
        self.assertIn('Abo-BezieherInnen', log.recipient_groups)
        self.assertIn('Anteilsschein-BesitzerInnen', log.recipient_groups)
        self.assertIn('Einzelne Mitglieder', log.recipient_groups)
        self.assertIn('Tätigkeitsbereiche', log.recipient_groups)
        self.assertIn('Einsätze', log.recipient_groups)
        self.assertIn('Depots', log.recipient_groups)
        self.assertIn('Kopie an Absender', log.recipient_groups)

    def test_alle_mail_send_pfade(self):
        paths = [
            '/email/write/',
            '/email/to/5/',
            '/email/depot/5/',
            '/email/area/3/',
            '/email/job/2/',
        ]
        for path in paths:
            EmailAuditLog.objects.all().delete()
            request = self.factory.post(path, {'submit': 'Senden', 'from_email': 'x@x.ch', 'subject': 'Test'})
            self.middleware(request)
            self.assertEqual(EmailAuditLog.objects.count(), 1, f'Kein Log-Eintrag für {path}')

    def test_kein_log_bei_get_request(self):
        request = self.factory.get('/email/write/')
        self.middleware(request)
        self.assertEqual(EmailAuditLog.objects.count(), 0)

    def test_kein_log_bei_anderem_pfad(self):
        request = self.factory.post('/my/profile', {'from_email': 'x@x.ch', 'submit': 'Senden'})
        self.middleware(request)
        self.assertEqual(EmailAuditLog.objects.count(), 0)

    def test_kein_log_bei_zaehl_endpunkt(self):
        # /email/depot/<id>/recipients/count ist ein AJAX-Zähl-Endpunkt, kein Versand
        request = self.factory.post('/email/depot/5/recipients/count', {'submit': 'x'})
        self.middleware(request)
        self.assertEqual(EmailAuditLog.objects.count(), 0)

    def test_kein_log_ohne_submit(self):
        # POST mit 'members' ohne 'submit' ist nur Vorbefüllen des Formulars, kein Versand
        request = self.factory.post('/email/write/', {'members': '1_2'})
        self.middleware(request)
        self.assertEqual(EmailAuditLog.objects.count(), 0)

    def test_fehlende_felder_verwenden_platzhalter(self):
        request = self.factory.post('/email/write/', {'submit': 'Senden'})
        self.middleware(request)
        log = EmailAuditLog.objects.get()
        self.assertEqual(log.sender, '–')
        self.assertEqual(log.subject, '–')
        self.assertEqual(log.recipient_groups, '–')
