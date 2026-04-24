from django.test import RequestFactory, TestCase

from gartenberg.middleware import EmailAuditMiddleware
from gartenberg.models import EmailAuditLog


class EmailAuditMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = EmailAuditMiddleware(get_response=lambda r: None)

    def test_erstellt_log_bei_mail_versand(self):
        request = self.factory.post('/my/mails/send', {
            'sender': 'laura@gartenberg.ch',
            'subject': 'Ernte-Info KW 17',
            'allsubscription': 'on',
        })
        self.middleware(request)
        self.assertEqual(EmailAuditLog.objects.count(), 1)
        log = EmailAuditLog.objects.get()
        self.assertEqual(log.sender, 'laura@gartenberg.ch')
        self.assertEqual(log.subject, 'Ernte-Info KW 17')
        self.assertIn('Abo-BezieherInnen', log.recipient_groups)
        self.assertEqual(log.url, '/my/mails/send')

    def test_alle_empfaenger_gruppen(self):
        request = self.factory.post('/my/mails/send', {
            'sender': 'info@gartenberg.ch',
            'subject': 'Test',
            'allsubscription': 'on',
            'allshares': 'on',
            'all': 'on',
            'allsingleemail': 'on',
            'recipients': 'extra@example.com',
        })
        self.middleware(request)
        log = EmailAuditLog.objects.get()
        self.assertIn('Abo-BezieherInnen', log.recipient_groups)
        self.assertIn('Anteilsschein-BesitzerInnen', log.recipient_groups)
        self.assertIn('Alle Mitglieder', log.recipient_groups)
        self.assertIn('Einzeladressen', log.recipient_groups)
        self.assertIn('Vorausgefüllte Adressen', log.recipient_groups)

    def test_alle_mail_send_pfade(self):
        paths = [
            '/my/mails/send',
            '/my/mails/send/depot',
            '/my/mails/send/area',
            '/my/mails/send/job',
        ]
        for path in paths:
            EmailAuditLog.objects.all().delete()
            request = self.factory.post(path, {'sender': 'x@x.ch', 'subject': 'Test'})
            self.middleware(request)
            self.assertEqual(EmailAuditLog.objects.count(), 1, f'Kein Log-Eintrag für {path}')

    def test_kein_log_bei_get_request(self):
        request = self.factory.get('/my/mails/send')
        self.middleware(request)
        self.assertEqual(EmailAuditLog.objects.count(), 0)

    def test_kein_log_bei_anderem_pfad(self):
        request = self.factory.post('/my/profile', {'sender': 'x@x.ch'})
        self.middleware(request)
        self.assertEqual(EmailAuditLog.objects.count(), 0)

    def test_fehlende_felder_verwenden_platzhalter(self):
        request = self.factory.post('/my/mails/send', {})
        self.middleware(request)
        log = EmailAuditLog.objects.get()
        self.assertEqual(log.sender, '–')
        self.assertEqual(log.subject, '–')
        self.assertEqual(log.recipient_groups, '–')
