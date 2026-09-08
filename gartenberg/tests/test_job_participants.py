import datetime

from django.contrib.auth.models import Permission
from django.test import TestCase, override_settings
from django.utils import timezone

from juntagrico.entity.jobs import ActivityArea, Assignment, JobType, RecuringJob
from juntagrico.entity.location import Location
from juntagrico.entity.member import Member
from juntagrico.util import addons
from juntagrico_assignment_request.models import AssignmentRequest


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
