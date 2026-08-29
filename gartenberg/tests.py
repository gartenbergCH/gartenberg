import datetime
from unittest.mock import patch

from django.contrib.auth.models import Permission
from django.core.files.storage import InMemoryStorage
from django.core.management import call_command
from django.template.loader import get_template
from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone

from juntagrico.entity.depot import Depot
from juntagrico.entity.jobs import ActivityArea, Assignment, JobType, RecuringJob
from juntagrico.entity.location import Location
from juntagrico.entity.member import Member
from juntagrico.entity.subs import Subscription, SubscriptionPart
from juntagrico.entity.subtypes import (
    ProductSize, SubscriptionBundle, SubscriptionBundleProductSize, SubscriptionCategory, SubscriptionProduct,
    SubscriptionType,
)
from juntagrico.util import addons
from juntagrico_assignment_request.models import AssignmentRequest

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


@override_settings(
    # base.html zieht die juntagrico-Assets über {% static %}; die ManifestStaticFilesStorage
    # aus den Projekt-Settings verlangt dafür ein zuvor erzeugtes collectstatic-Manifest.
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    },
)
class JobParticipantsViewTest(TestCase):
    """Einsatzliste mit den eingeschriebenen Personen (UC-010)."""

    url = '/einsatzliste/'

    @classmethod
    def setUpTestData(cls):
        location = Location.objects.create(name='auf dem Hof')
        cls.verteilung = ActivityArea.objects.create(name='Ernteverteilung', sort_order=1)
        cls.anbau = ActivityArea.objects.create(name='Gemüseanbau', sort_order=2)
        cls.abpacken = JobType.objects.create(
            name='Ernteverteilung - Abpacken', activityarea=cls.verteilung,
            default_duration=2, location=location,
        )
        cls.verteilfahrt = JobType.objects.create(
            name='Ernteverteilung - Verteilfahrt', activityarea=cls.verteilung,
            default_duration=3, location=location,
        )
        cls.setzlingsfahrt = JobType.objects.create(
            name='Gemüseanbau - Setzlingsfahrt', activityarea=cls.anbau,
            default_duration=4, location=location,
        )

        cls.morgen = timezone.now() + datetime.timedelta(days=1)
        cls.job_abpacken = RecuringJob.objects.create(type=cls.abpacken, slots=4, time=cls.morgen)
        cls.job_verteilfahrt = RecuringJob.objects.create(
            type=cls.verteilfahrt, slots=2, time=cls.morgen + datetime.timedelta(days=1),
        )
        cls.job_setzlingsfahrt = RecuringJob.objects.create(
            type=cls.setzlingsfahrt, slots=2, time=cls.morgen + datetime.timedelta(days=2),
        )
        cls.job_vergangen = RecuringJob.objects.create(
            type=cls.abpacken, slots=4, time=timezone.now() - datetime.timedelta(days=3),
        )

        cls.anna = cls._make_member('Anna', 'Zwahlen', '079 111 11 11')
        cls.beat = cls._make_member('Beat', 'Amsler', '079 222 22 22')
        # Anna belegt zwei Plätze desselben Einsatzes -> zwei Assignments, ein Listeneintrag
        Assignment.objects.create(job=cls.job_abpacken, member=cls.anna, amount=1)
        Assignment.objects.create(job=cls.job_abpacken, member=cls.anna, amount=1)
        Assignment.objects.create(job=cls.job_abpacken, member=cls.beat, amount=1)

        cls.koordination = cls._make_member('Karin', 'Oberli', '079 333 33 33')
        cls.koordination.user.user_permissions.add(
            Permission.objects.get(codename='view_assignment', content_type__app_label='juntagrico')
        )

    @classmethod
    def _make_member(cls, first_name, last_name, phone):
        return Member.objects.create(
            first_name=first_name, last_name=last_name,
            email=f'{first_name.lower()}@e2e-test.local',
            addr_street='Teststrasse 1', addr_zipcode='5000', addr_location='Aarau',
            phone=phone, confirmed=True, reachable_by_email=False,
        )

    def _get(self, **params):
        self.client.force_login(self.koordination.user)
        return self.client.get(self.url, params)

    def _listed_jobs(self, response):
        return [row['job'] for row in response.context['rows']]

    def test_ohne_berechtigung_kein_zugriff(self):
        # Kontaktangaben der Eingeschriebenen sind nur für Berechtigte sichtbar (GR-004)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.anna.user)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_zeigt_nur_kuenftige_einsaetze_chronologisch(self):
        # GR-001 (nur künftige Einsätze) und GR-002 (chronologisch)
        response = self._get()
        self.assertEqual(
            self._listed_jobs(response),
            [self.job_abpacken, self.job_verteilfahrt, self.job_setzlingsfahrt],
        )

    def test_zeigt_eingeschriebene_mit_kontaktangaben(self):
        response = self._get()
        participants = response.context['rows'][0]['participants']
        # Nach Nachname sortiert; Anna erscheint trotz zweier Assignments nur einmal
        self.assertEqual([p['member'] for p in participants], [self.beat, self.anna])
        self.assertEqual([p['slots'] for p in participants], [1, 2])

        content = response.content.decode()
        self.assertIn('Zwahlen, Anna', content)
        self.assertIn('anna@e2e-test.local', content)
        self.assertIn('079 111 11 11', content)

    def test_einsatz_ohne_anmeldungen_bleibt_sichtbar(self):
        # A1: offene Termine müssen auffallen, nicht verschwinden
        response = self._get()
        self.assertEqual(response.context['rows'][2]['participants'], [])
        self.assertIn('noch niemand eingeschrieben', response.content.decode())

    def test_abgesagter_einsatz_wird_gekennzeichnet(self):
        # A2: der Termin bleibt sichtbar, damit die Koordination die Absage bemerkt
        self.job_verteilfahrt.canceled = True
        self.job_verteilfahrt.save()
        response = self._get()
        self.assertIn(self.job_verteilfahrt, self._listed_jobs(response))
        self.assertIn('abgesagt', response.content.decode())

    def test_filter_auf_taetigkeitsbereich(self):
        response = self._get(scope=f'area:{self.verteilung.id}')
        self.assertEqual(
            self._listed_jobs(response), [self.job_abpacken, self.job_verteilfahrt]
        )
        self.assertEqual(response.context['selected_scope'], f'area:{self.verteilung.id}')

    def test_filter_auf_einsatzart(self):
        response = self._get(scope=f'type:{self.setzlingsfahrt.id}')
        self.assertEqual(self._listed_jobs(response), [self.job_setzlingsfahrt])

    def test_unbrauchbarer_filter_zeigt_alle_einsaetze(self):
        # Ein Lesezeichen auf einen gelöschten Bereich darf keinen Fehler auslösen
        for scope in ('kaputt', 'area:', 'area:abc', 'type:999999'):
            with self.subTest(scope=scope):
                response = self._get(scope=scope)
                self.assertEqual(response.status_code, 200)
                if scope == 'type:999999':
                    self.assertEqual(self._listed_jobs(response), [])
                else:
                    self.assertEqual(len(self._listed_jobs(response)), 3)
                    self.assertEqual(response.context['selected_scope'], '')

    def test_auswahl_stammt_aus_der_datenbank(self):
        # GR-003: keine im Code verdrahteten Einsatzarten
        response = self._get()
        areas, job_types = response.context['scope_choices']
        self.assertEqual(
            [option['label'] for option in areas[1]], ['Ernteverteilung', 'Gemüseanbau']
        )
        self.assertIn(
            {'value': f'type:{self.abpacken.id}', 'label': 'Ernteverteilung – Ernteverteilung - Abpacken'},
            job_types[1],
        )

    def test_einsatzmeldungen_erscheinen_nicht(self):
        # juntagrico-assignment-request legt für jede bestätigte Meldung im Hintergrund
        # einen Einsatz an. Er ist nicht ausgeschrieben und gehört nicht auf die Liste.
        AssignmentRequest.objects.create(
            member=self.beat, status=AssignmentRequest.CONFIRMED,
            job_time=self.morgen, duration=2,
        )
        gemeldeter_einsatz = Assignment.objects.exclude(job__in=[
            self.job_abpacken, self.job_verteilfahrt, self.job_setzlingsfahrt,
        ]).get().job
        response = self._get()
        self.assertNotIn(gemeldeter_einsatz, self._listed_jobs(response))
        self.assertNotIn(
            'Selbständiger Einsatz',
            [option['label'] for option in response.context['scope_choices'][1][1]],
        )

    def test_menueeintrag_ist_registriert(self):
        self.assertIn('gartenberg/menu/admin/job_participants.html', addons.config.get_admin_menus())
