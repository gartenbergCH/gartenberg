import datetime
import re

from django.test import TestCase, override_settings

from juntagrico.entity.depot import Depot
from juntagrico.entity.jobs import ActivityArea, Assignment, JobType, RecuringJob
from juntagrico.entity.location import Location
from juntagrico.entity.member import Member
from juntagrico.entity.subs import Subscription, SubscriptionPart
from juntagrico.entity.subtypes import (
    ProductSize, SubscriptionBundle, SubscriptionBundleProductSize, SubscriptionCategory, SubscriptionProduct,
    SubscriptionType,
)
from juntagrico.util.temporal import start_of_business_year


@override_settings(
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    },
)
class ManageAssignmentsViewTest(TestCase):
    """Einsatzübersicht der Verwaltung mit "E-Mails unter 100 % kopieren" (UC-013)."""

    url = '/manage/assignments'

    @classmethod
    def setUpTestData(cls):
        location = Location.objects.create(name='Hof')
        depot = Depot.objects.create(name='Hofdepot', weekday=2, location=location)
        product = SubscriptionProduct.objects.create(name='Gemüse')
        product_size = ProductSize.objects.create(name='Normal', product=product)
        bundle = SubscriptionBundle.objects.create(
            long_name='Gemüse Abo', category=SubscriptionCategory.objects.create(name='Kategorie'),
        )
        SubscriptionBundleProductSize.objects.create(bundle=bundle, product_size=product_size)
        sub_type = SubscriptionType.objects.create(name='Gemüse-Typ', bundle=bundle, required_assignments=4, price=100)

        start = start_of_business_year()
        today = datetime.date.today()
        cls.anna, cls.anna_sub = cls._make_subscriber('Anna', 'Zwahlen', depot, sub_type, start)
        # Gekündigt, aber noch nicht deaktiviert: soll weiterhin angeschrieben werden
        _, cls.gekuendigt = cls._make_subscriber('Gerda', 'Kuendig', depot, sub_type, start)
        cls.gekuendigt.cancellation_date = today
        cls.gekuendigt.save()
        # Bereits deaktiviert: mit dem Mitglied direkt gelöst (GR-003)
        _, cls.deaktiviert = cls._make_subscriber('Dieter', 'Weg', depot, sub_type, start)
        cls.deaktiviert.cancellation_date = today - datetime.timedelta(days=1)
        cls.deaktiviert.deactivation_date = today - datetime.timedelta(days=1)
        cls.deaktiviert.save()

        job_type = JobType.objects.create(
            name='Abpacken', activityarea=ActivityArea.objects.create(name='Ernteverteilung'),
            default_duration=2, location=location,
        )
        job = RecuringJob.objects.create(type=job_type, slots=4, time=datetime.datetime.combine(
            start + datetime.timedelta(days=1), datetime.time(9), tzinfo=datetime.UTC,
        ))
        Assignment.objects.create(job=job, member=cls.anna, amount=1.5)

        cls.admin = Member.objects.create(
            first_name='Karin', last_name='Oberli', email='karin@e2e-test.local',
            addr_street='Teststrasse 1', addr_zipcode='5000', addr_location='Aarau',
            phone='079 333 33 33', confirmed=True, reachable_by_email=False,
        ).user
        cls.admin.is_superuser = True
        cls.admin.save()

    @classmethod
    def _make_subscriber(cls, first_name, last_name, depot, sub_type, start):
        subscription = Subscription.objects.create(depot=depot, activation_date=start, start_date=start)
        SubscriptionPart.objects.create(subscription=subscription, type=sub_type, activation_date=start)
        member = Member.objects.create(
            first_name=first_name, last_name=last_name, email=f'{first_name.lower()}@e2e-test.local',
            addr_street='Teststrasse 1', addr_zipcode='5000', addr_location='Aarau',
            phone='079 111 11 11', confirmed=True, reachable_by_email=False,
        )
        member.join_subscription(subscription, True)
        # Einsätze zählen nur ab dem Beitritt zum Abo
        subscription.subscriptionmembership_set.update(join_date=start)
        return member, subscription

    def _content(self):
        self.client.force_login(self.admin)
        return self.client.get(self.url).content.decode()

    def test_zeigt_schaltflaeche_fuer_e_mails_unter_100_prozent(self):
        content = self._content()
        self.assertIn('E-Mails unter 100 % kopieren', content)
        # Die Schaltfläche ergänzt die bestehenden, ersetzt sie aber nicht
        self.assertIn('email_copy_button()', content)

    def test_spalten_liegen_an_den_im_skript_erwarteten_positionen(self):
        # Das Skript liest die Abo-Id aus dem Admin-Link der 3. Spalte (Index 2) und den Status
        # aus der 6. Spalte (Index 5) mit deutschem Dezimalkomma. Ändert juntagrico das
        # Template, soll dieser Test anschlagen (GR-001, GR-003).
        content = self._content()
        self.assertIn('const status_column = 2', content)
        self.assertIn('const progress_column = 5', content)
        row = next(
            r for r in re.findall(r'<tr>(.*?)</tr>', content, re.S) if 'anna@e2e-test.local' in r
        )
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
        self.assertRegex(cells[2], rf'href="[^"]*subscription/{self.anna_sub.id}/')
        self.assertEqual(cells[5].strip(), '37,5%')

    def test_nur_bereits_deaktivierte_abos_werden_ausgenommen(self):
        # GR-003: deaktiviert -> ausgenommen, gekündigt oder aktiv -> weiterhin dabei
        content = self._content()
        deactivated = re.search(r'const deactivated_subscriptions = new Set\(\[(.*?)\]\)', content).group(1)
        self.assertEqual(re.findall(r"'(\d+)'", deactivated), [str(self.deaktiviert.id)])
