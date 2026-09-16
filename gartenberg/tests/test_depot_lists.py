import datetime
import importlib
import re
from unittest.mock import patch

from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.files.storage import InMemoryStorage
from django.core.management import call_command
from django.template.loader import get_template
from django.test import TestCase, override_settings

from juntagrico.entity.depot import Depot
from juntagrico.entity.location import Location
from juntagrico.entity.member import Member
from juntagrico.entity.subs import Subscription, SubscriptionPart
from juntagrico.entity.subtypes import (
    ProductSize, SubscriptionBundle, SubscriptionBundleProductSize, SubscriptionCategory, SubscriptionProduct,
    SubscriptionType,
)

from gartenberg.depot_lists import DEPOT_LISTS
from gartenberg.models import SubscriptionTypeProductSize


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
        # Absichtlich nicht-alphabetisch angelegt, damit die Sortierung nicht zufällig
        # mit der Einfügereihenfolge übereinstimmt
        cls.gemuese_zora = cls._add_subscriber_to_product('Gemüse', 'Zora')
        cls.gemuese_anna = cls._add_subscriber_to_product('Gemüse', 'anna')
        cls.gemuese_bea = cls._add_subscriber_to_product('Gemüse', 'Bea')

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

    @classmethod
    def _add_subscriber_to_product(cls, product_name, first_name):
        sub_type = SubscriptionType.objects.get(name=f'{product_name}-Typ')
        today = datetime.date.today()
        member = Member.objects.create(
            first_name=first_name, last_name='Testperson',
            email=f'{first_name.lower()}@e2e-test.local',
            addr_street='Teststrasse 1', addr_zipcode='5000', addr_location='Aarau',
            phone='079 000 00 00', confirmed=True, reachable_by_email=False,
        )
        subscription = Subscription.objects.create(depot=cls.depot, activation_date=today, start_date=today)
        SubscriptionPart.objects.create(subscription=subscription, type=sub_type, activation_date=today)
        member.join_subscription(subscription, True)
        return subscription

    def test_subscriptions_sind_alphabetisch_sortiert(self):
        # FR-052 / UC-004 GR-007: Bezüger/innen je Depot alphabetisch.
        # Regression: der produktgefilterte extra_context überschreibt den Basis-Kontext von
        # juntagrico.util.depot_list.depot_list_data und verlor dabei dessen Sortierung, wodurch
        # die Personenliste pro Depot in beliebiger DB-Reihenfolge erschien.
        context = {'date': datetime.date.today()}
        gemuese_context = DEPOT_LISTS['depotlist']['extra_context'](context)
        first_names = [sub.primary_member.first_name for sub in gemuese_context['subscriptions']]
        # Sortierung case-insensitiv, wie in juntagrico
        self.assertEqual(first_names, ['anna', 'Bea', 'Gemüse', 'Zora'])

    def test_extra_context_filters_by_product(self):
        context = {'date': datetime.date.today()}

        kartoffeln_context = DEPOT_LISTS['depotlist_kartoffeln']['extra_context'](context)
        self.assertCountEqual(kartoffeln_context['subscriptions'], [self.kartoffeln_sub])
        self.assertCountEqual(kartoffeln_context['products'].values_list('name', flat=True), ['Kartoffeln'])

        # Haupt-, Depot- und Mengenübersicht bleiben wie bisher auf Gemüse beschränkt,
        # damit sie durch die Hofprodukte-Kategorien nicht überladen werden
        for list_name in ('depotlist', 'depot_overview', 'amount_overview'):
            gemuese_context = DEPOT_LISTS[list_name]['extra_context'](context)
            self.assertCountEqual(
                gemuese_context['subscriptions'],
                [self.gemuese_sub, self.gemuese_zora, self.gemuese_anna, self.gemuese_bea],
            )
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


@override_settings(DEPOT_LISTS=DEPOT_LISTS)
class DepotListPartStateTest(TestCase):
    """FR-053 / UC-004 GR-006: Auf einer Produktliste erscheint ein Abo nur, wenn ein Bestandteil dieses
    Produkts am Stichtag aktiv ist. Regression: bisher genügte ein aktives Abo, womit Abos mit
    nur bestelltem oder bereits deaktiviertem Mehl-Bestandteil als leere Zeile erschienen."""

    STICHTAG = datetime.date(2026, 9, 16)

    @classmethod
    def setUpTestData(cls):
        location = Location.objects.create(name='Hof')
        cls.depot = Depot.objects.create(name='Hofdepot', weekday=2, location=location)
        category = SubscriptionCategory.objects.create(name='Hofprodukte')
        gemuese = SubscriptionProduct.objects.create(name='Gemüse')
        gemuese_bundle = SubscriptionBundle.objects.create(long_name='1 Ernteanteil', category=category)
        SubscriptionBundleProductSize.objects.create(
            bundle=gemuese_bundle, product_size=ProductSize.objects.create(name='Ganz', product=gemuese),
        )
        cls.gemuese_type = SubscriptionType.objects.create(
            name='Ganz', bundle=gemuese_bundle, required_assignments=0, price=1465,
        )
        product = SubscriptionProduct.objects.create(name='Mehl')
        size = ProductSize.objects.create(name='Weizen HW 1kg', product=product)
        bundle = SubscriptionBundle.objects.create(long_name='Mehl', category=category)
        SubscriptionBundleProductSize.objects.create(bundle=bundle, product_size=size)
        cls.mehl_type = SubscriptionType.objects.create(
            name='Weizenmehl Halbweiss 1kg', bundle=bundle, required_assignments=0, price=17,
        )

    def _subscription_with_mehl_part(self, first_name, **part_dates):
        start = self.STICHTAG - datetime.timedelta(days=60)
        member = Member.objects.create(
            first_name=first_name, last_name='Testperson', email=f'{first_name.lower()}@e2e-test.local',
            addr_street='Teststrasse 1', addr_zipcode='5000', addr_location='Aarau',
            phone='079 000 00 00', confirmed=True, reachable_by_email=False,
        )
        subscription = Subscription.objects.create(depot=self.depot, activation_date=start, start_date=start)
        # Realer Fall: aktives Gemüse-Abo, zu dem Mehl bestellt wurde
        SubscriptionPart.objects.create(subscription=subscription, type=self.gemuese_type, activation_date=start)
        SubscriptionPart.objects.create(subscription=subscription, type=self.mehl_type, **part_dates)
        member.join_subscription(subscription, True)
        return subscription

    def _mehl_subscriptions(self):
        context = {'date': self.STICHTAG}
        return list(DEPOT_LISTS['depotlist_mehl']['extra_context'](context)['subscriptions'])

    def test_bestellter_bestandteil_erscheint_nicht(self):
        self._subscription_with_mehl_part('Bestellt')
        self.assertEqual(self._mehl_subscriptions(), [])

    def test_erst_nach_stichtag_aktivierter_bestandteil_erscheint_nicht(self):
        self._subscription_with_mehl_part('Spaeter', activation_date=self.STICHTAG + datetime.timedelta(days=1))
        self.assertEqual(self._mehl_subscriptions(), [])

    def test_aktiver_bestandteil_erscheint(self):
        sub = self._subscription_with_mehl_part('Aktiv', activation_date=self.STICHTAG - datetime.timedelta(days=30))
        self.assertEqual(self._mehl_subscriptions(), [sub])

    def test_gekuendigter_nicht_deaktivierter_bestandteil_erscheint(self):
        sub = self._subscription_with_mehl_part(
            'Gekuendigt',
            activation_date=self.STICHTAG - datetime.timedelta(days=30),
            cancellation_date=self.STICHTAG - datetime.timedelta(days=5),
        )
        self.assertEqual(self._mehl_subscriptions(), [sub])

    def test_gekuendigter_erst_nach_stichtag_deaktivierter_bestandteil_erscheint(self):
        sub = self._subscription_with_mehl_part(
            'Auslaufend',
            activation_date=self.STICHTAG - datetime.timedelta(days=30),
            cancellation_date=self.STICHTAG - datetime.timedelta(days=5),
            deactivation_date=self.STICHTAG + datetime.timedelta(days=10),
        )
        self.assertEqual(self._mehl_subscriptions(), [sub])

    def test_deaktivierter_bestandteil_erscheint_nicht(self):
        self._subscription_with_mehl_part(
            'Deaktiviert',
            activation_date=self.STICHTAG - datetime.timedelta(days=30),
            cancellation_date=self.STICHTAG - datetime.timedelta(days=20),
            deactivation_date=self.STICHTAG - datetime.timedelta(days=1),
        )
        self.assertEqual(self._mehl_subscriptions(), [])

    def test_zeile_zaehlt_nur_aktive_bestandteile(self):
        sub = self._subscription_with_mehl_part('Gemischt', activation_date=self.STICHTAG - datetime.timedelta(days=30))
        # zusätzlich ein bestellter und ein deaktivierter Bestandteil derselben Grösse
        SubscriptionPart.objects.create(subscription=sub, type=self.mehl_type)
        SubscriptionPart.objects.create(
            subscription=sub, type=self.mehl_type,
            activation_date=self.STICHTAG - datetime.timedelta(days=30),
            cancellation_date=self.STICHTAG - datetime.timedelta(days=20),
            deactivation_date=self.STICHTAG - datetime.timedelta(days=1),
        )
        context = {'date': self.STICHTAG, 'depots': [self.depot], 'messages': []}
        html = get_template('exports/depotlist_compact.html').render(
            context | DEPOT_LISTS['depotlist_mehl']['extra_context'](context)
        )
        self.assertEqual(html.count('Gemischt'), 1)
        self.assertRegex(html, r'Gemischt[\s\S]*?<td class="top-border left-border right-border">1</td>')


@override_settings(DEPOT_LISTS=DEPOT_LISTS)
class DepotListProductSizeTest(TestCase):
    """FR-054, FR-055 / UC-004 GR-008, GR-009: Ein Bestandteil zählt nur in der Spalte seiner Produktgrösse.
    Regression: Das Paket "Mehl" enthält alle Mehl-Grössen, weshalb juntagrico jeden
    Mehl-Bestandteil in jeder Mehl-Spalte zählte (4 Bestandteile → überall eine 4)."""

    STICHTAG = datetime.date(2026, 9, 16)
    START = datetime.date(2026, 1, 1)

    @classmethod
    def setUpTestData(cls):
        location = Location.objects.create(name='Hof')
        cls.depot = Depot.objects.create(name='Hofdepot', weekday=2, location=location)
        category = SubscriptionCategory.objects.create(name='Hofprodukte')
        gemuese = SubscriptionProduct.objects.create(name='Gemüse')
        gemuese_bundle = SubscriptionBundle.objects.create(long_name='1 Ernteanteil', category=category)
        cls.gemuese_size = ProductSize.objects.create(name='Ganz', product=gemuese)
        SubscriptionBundleProductSize.objects.create(bundle=gemuese_bundle, product_size=cls.gemuese_size)
        cls.gemuese_type = SubscriptionType.objects.create(
            name='Ganz', bundle=gemuese_bundle, required_assignments=0, price=1465,
        )

        mehl = SubscriptionProduct.objects.create(name='Mehl')
        cls.mehl_bundle = SubscriptionBundle.objects.create(long_name='Mehl', category=category)
        cls.sizes = {}
        cls.types = {}
        for sort_order, (size_name, type_name) in enumerate([
            ('Weizen HW 1kg', 'Weizenmehl Halbweiss 1kg'),
            ('Weizen HW 3kg', 'Weizenmehl Halbweiss 3kg'),
            ('Weizen Ruch 1kg', 'Weizenmehl Ruch 1kg'),
            ('Dinkel HW 1kg', 'Dinkelmehl Halbweiss 1kg'),
        ]):
            size = ProductSize.objects.create(name=size_name, product=mehl, sort_order=sort_order)
            SubscriptionBundleProductSize.objects.create(bundle=cls.mehl_bundle, product_size=size)
            cls.sizes[size_name] = size
            cls.types[type_name] = SubscriptionType.objects.create(
                name=type_name, bundle=cls.mehl_bundle, required_assignments=0, price=20,
            )
        seed = importlib.import_module('gartenberg.migrations.0003_seed_subscriptiontypeproductsize').seed
        seed(apps, None)

        cls.sub = cls._subscription('Anna', [
            'Weizenmehl Halbweiss 3kg', 'Weizenmehl Halbweiss 3kg', 'Weizenmehl Ruch 1kg', 'Dinkelmehl Halbweiss 1kg',
        ])

    @classmethod
    def _subscription(cls, first_name, mehl_type_names):
        member = Member.objects.create(
            first_name=first_name, last_name='Testperson', email=f'{first_name.lower()}@e2e-test.local',
            addr_street='Teststrasse 1', addr_zipcode='5000', addr_location='Aarau',
            phone='079 000 00 00', confirmed=True, reachable_by_email=False,
        )
        subscription = Subscription.objects.create(depot=cls.depot, activation_date=cls.START, start_date=cls.START)
        SubscriptionPart.objects.create(subscription=subscription, type=cls.gemuese_type, activation_date=cls.START)
        for type_name in mehl_type_names:
            SubscriptionPart.objects.create(
                subscription=subscription, type=cls.types[type_name], activation_date=cls.START,
            )
        member.join_subscription(subscription, True)
        return subscription

    def _render_mehl_list(self):
        context = {'date': self.STICHTAG, 'depots': [self.depot], 'messages': []}
        extra_context = DEPOT_LISTS['depotlist_mehl']['extra_context'](context)
        html = get_template('exports/depotlist_compact.html').render(context | extra_context)
        return html, extra_context

    @staticmethod
    def _row_cells(html, first_name):
        row = re.search(rf'<tr class="bottom-border">\s*<td class="namecol[^>]*>[\s\S]*?{first_name}[\s\S]*?</tr>', html)
        return re.findall(r'<td class="top-border left-border[^"]*">([^<]*)</td>', row.group(0))

    @staticmethod
    def _total_cells(html):
        row = re.search(r'TOTAL:</td>([\s\S]*?)</tr>', html)
        return re.findall(r'<td>([^<]*)</td>', row.group(1))

    def test_seed_ordnet_typen_ihrer_groesse_zu(self):
        self.assertEqual(
            SubscriptionTypeProductSize.objects.get(subscription_type=self.types['Weizenmehl Halbweiss 3kg']).product_size,
            self.sizes['Weizen HW 3kg'],
        )
        self.assertEqual(SubscriptionTypeProductSize.objects.count(), 4)

    def test_menge_je_groesse_pro_abo_und_total(self):
        # Spalten in Sortierreihenfolge: Weizen HW 1kg, Weizen HW 3kg, Weizen Ruch 1kg, Dinkel HW 1kg
        html, extra_context = self._render_mehl_list()
        self.assertEqual(self._row_cells(html, 'Anna'), ['', '2', '1', '1'])
        self.assertEqual(self._total_cells(html), ['0', '2', '1', '1'])
        self.assertEqual(extra_context['messages'], [])

    def test_gemuese_ohne_zuordnung_zaehlt_wie_bisher(self):
        # Paket mit nur einer Grösse des Produkts braucht keine Zuordnung
        context = {'date': self.STICHTAG, 'depots': [self.depot], 'messages': []}
        html = get_template('exports/depotlist.html').render(
            context | DEPOT_LISTS['depotlist']['extra_context'](context)
        )
        row = re.search(r'Anna[\s\S]*?</tr>', html).group(0)
        self.assertEqual(re.findall(r'<td class="top-border left-border">([^<]*)</td>', row)[0], '1')

    def test_typ_ohne_zuordnung_wird_nicht_gezaehlt_und_gemeldet(self):
        SubscriptionTypeProductSize.objects.filter(subscription_type=self.types['Weizenmehl Ruch 1kg']).delete()
        html, extra_context = self._render_mehl_list()
        self.assertEqual(self._row_cells(html, 'Anna'), ['', '2', '', '1'])
        self.assertEqual(extra_context['messages'], [
            'Abo-Typ "Hofprodukte - Mehl-Weizenmehl Ruch 1kg" hat keine Produktgrösse auf '
            'Depotliste zugeordnet und wird nicht gezählt.',
        ])
        self.assertIn('Weizenmehl Ruch 1kg', html)

    def test_listenhinweise_aus_admin_bleiben_erhalten(self):
        context = {'date': self.STICHTAG, 'messages': ['Bitte Taschen zurückbringen']}
        extra_context = DEPOT_LISTS['depotlist_mehl']['extra_context'](context)
        self.assertEqual(extra_context['messages'], ['Bitte Taschen zurückbringen'])

    @override_settings(STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'},
        'staticfiles': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    })
    def test_zuordnung_im_admin_des_abo_typs_pflegbar(self):
        from django.contrib.auth.models import User
        from django.urls import reverse
        admin_user = User.objects.create_superuser('admin', 'admin@e2e-test.local', 'pw')
        self.client.force_login(admin_user)
        response = self.client.get(
            reverse('admin:juntagrico_subscriptiontype_change', args=[self.types['Weizenmehl Ruch 1kg'].pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Produktgrösse auf Depotliste')

    def test_zuordnung_muss_im_paket_enthalten_sein(self):
        mapping = SubscriptionTypeProductSize(
            subscription_type=self.types['Weizenmehl Ruch 1kg'], product_size=self.gemuese_size,
        )
        with self.assertRaises(ValidationError):
            mapping.clean()
