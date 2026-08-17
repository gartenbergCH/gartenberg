import datetime
from unittest.mock import patch

from django.core.files.storage import InMemoryStorage
from django.core.management import call_command
from django.template.loader import get_template
from django.test import RequestFactory, TestCase, override_settings

from juntagrico.entity.depot import Depot
from juntagrico.entity.location import Location
from juntagrico.entity.member import Member
from juntagrico.entity.subs import Subscription, SubscriptionPart
from juntagrico.entity.subtypes import (
    ProductSize, SubscriptionBundle, SubscriptionBundleProductSize, SubscriptionCategory, SubscriptionProduct,
    SubscriptionType,
)

from gartenberg.depot_lists import DEPOT_LISTS
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


@override_settings(
    DEPOT_LISTS=DEPOT_LISTS,
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'},
        'staticfiles': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    },
)
class DepotListsPerCategoryTest(TestCase):
    """Stellt sicher, dass die in gartenberg/depot_lists.py definierten Hofprodukte-Listen
    (Kartoffeln, Mehl, Glarner Alpkäse) generiert werden können und korrekt nach Produkt filtern."""

    @classmethod
    def setUpTestData(cls):
        location = Location.objects.create(name='Hof')
        cls.depot = Depot.objects.create(name='Hofdepot', weekday=2, location=location)
        cls.category = SubscriptionCategory.objects.create(name='Kategorie')
        cls.gemuese_sub = cls._make_subscriber('Gemüse')
        cls.kartoffeln_sub = cls._make_subscriber('Kartoffeln')

    @classmethod
    def _make_subscriber(cls, product_name):
        product = SubscriptionProduct.objects.create(name=product_name)
        product_size = ProductSize.objects.create(name='Normal', product=product)
        bundle = SubscriptionBundle.objects.create(long_name=f'{product_name} Abo', category=cls.category)
        SubscriptionBundleProductSize.objects.create(bundle=bundle, product_size=product_size)
        sub_type = SubscriptionType.objects.create(
            name=f'{product_name}-Typ', bundle=bundle, required_assignments=0, price=100,
        )
        today = datetime.date.today()
        member = Member.objects.create(
            first_name=product_name, last_name='Testperson', email=f'{product_name.lower()}@e2e-test.local',
            addr_street='Teststrasse 1', addr_zipcode='5000', addr_location='Aarau',
            phone='079 000 00 00', confirmed=True, reachable_by_email=False,
        )
        subscription = Subscription.objects.create(depot=cls.depot, activation_date=today, start_date=today)
        SubscriptionPart.objects.create(subscription=subscription, type=sub_type, activation_date=today)
        member.join_subscription(subscription, True)
        return subscription

    def test_extra_context_filters_by_product(self):
        context = {'date': datetime.date.today()}

        kartoffeln_context = DEPOT_LISTS['depotlist_kartoffeln']['extra_context'](context)
        self.assertCountEqual(kartoffeln_context['subscriptions'], [self.kartoffeln_sub])
        self.assertCountEqual(kartoffeln_context['products'].values_list('name', flat=True), ['Kartoffeln'])

        # Haupt-, Depot- und Mengenübersicht bleiben wie bisher auf Gemüse beschränkt,
        # damit sie durch die Hofprodukte-Kategorien nicht überladen werden
        for list_name in ('depotlist', 'depot_overview', 'amount_overview'):
            gemuese_context = DEPOT_LISTS[list_name]['extra_context'](context)
            self.assertCountEqual(gemuese_context['subscriptions'], [self.gemuese_sub])
            self.assertCountEqual(gemuese_context['products'].values_list('name', flat=True), ['Gemüse'])

        # Kategorien ohne Bestellungen liefern eine leere Liste statt eines Fehlers
        for list_name in ('depotlist_mehl', 'depotlist_alpkaese'):
            empty_context = DEPOT_LISTS[list_name]['extra_context'](context)
            self.assertCountEqual(empty_context['subscriptions'], [])
            self.assertCountEqual(empty_context['products'], [])

    def test_generate_depot_list_command_creates_all_category_pdfs(self):
        # juntagrico legt die PDFs im 'internal' Storage ab (juntagrico.util.pdf.internal_storage),
        # nicht im default Storage. Da dieser LazyObject-Wrapper seinen Storage beim ersten Zugriff
        # cached, lässt er sich nicht über die STORAGES-Settings umbiegen — deshalb hier ersetzen,
        # sonst würden die PDFs ins Verzeichnis internal_files/ im Repo geschrieben.
        internal_storage = InMemoryStorage()
        with patch('juntagrico.util.pdf.internal_storage', internal_storage):
            call_command('generate_depot_list', '--force', '--no-future')
        file_names = (
            'depotlist', 'depot_overview', 'amount_overview',
            'depotlist_kartoffeln', 'depotlist_mehl', 'depotlist_alpkaese',
        )
        for file_name in file_names:
            self.assertTrue(internal_storage.exists(f'{file_name}.pdf'), f'{file_name}.pdf wurde nicht erzeugt')

    def test_mehl_und_alpkaese_verwenden_kompaktes_template(self):
        # Mehl (10 Produktgrössen) und Glarner Alpkäse (8) sprengen das Standard-Layout mit
        # "abgeholt"/"Tasche retour"-Spalten; Gemüse und Kartoffeln bleiben unverändert.
        self.assertEqual(DEPOT_LISTS['depotlist_mehl']['template'], 'exports/depotlist_compact.html')
        self.assertEqual(DEPOT_LISTS['depotlist_alpkaese']['template'], 'exports/depotlist_compact.html')
        self.assertEqual(DEPOT_LISTS['depotlist']['template'], 'exports/depotlist.html')
        self.assertEqual(DEPOT_LISTS['depotlist_kartoffeln']['template'], 'exports/depotlist.html')

        context = {'date': datetime.date.today(), 'depots': [self.depot], 'messages': []}
        compact_html = get_template('exports/depotlist_compact.html').render(
            context | DEPOT_LISTS['depotlist_mehl']['extra_context'](context)
        )
        self.assertNotIn('abgeholt', compact_html)

        regular_html = get_template('exports/depotlist.html').render(
            context | DEPOT_LISTS['depotlist']['extra_context'](context)
        )
        self.assertIn('abgeholt', regular_html)
