import datetime

from django.test import TestCase

from juntagrico.entity.depot import Depot
from juntagrico.entity.location import Location
from juntagrico.entity.member import Member, SubscriptionMembership
from juntagrico.entity.subs import Subscription, SubscriptionPart
from juntagrico.entity.subtypes import SubscriptionBundle, SubscriptionCategory, SubscriptionType

from gartenberg.email_forms import CategoryRecipientsForm, members_with_active_subscription_in_categories
from gartenberg.middleware import EmailAuditMiddleware
from gartenberg.models import EmailAuditLog

TODAY = datetime.date.today()
DAY = datetime.timedelta(days=1)


class MembersInCategoryTest(TestCase):
    """UC-005 GR-007 / FR-057: Empfänger/innen nach Abokategorie."""

    @classmethod
    def setUpTestData(cls):
        cls.depot = Depot.objects.create(name='Depot', weekday=2, location=Location.objects.create(name='Hof'))
        cls.gemuese = SubscriptionCategory.objects.create(name='Gemüse')
        cls.hof = SubscriptionCategory.objects.create(name='Hofprodukte')
        cls.types = {}
        for category in (cls.gemuese, cls.hof, None):
            bundle = SubscriptionBundle.objects.create(long_name=f'Paket {category}', category=category)
            cls.types[category] = SubscriptionType.objects.create(
                name=f'Typ {category}', bundle=bundle, required_assignments=0, price=1)

    def _member(self, name):
        return Member.objects.create(
            first_name=name, last_name='Test', email=f'{name.lower()}@e2e-test.local',
            addr_street='x 1', addr_zipcode='5000', addr_location='Aarau', phone='1', confirmed=True)

    def _subscriber(self, name, *categories, activation=TODAY, deactivation=None, part_activation=True,
                    part_deactivation=None, cancelled=False, leave=None):
        member = self._member(name)
        sub = Subscription.objects.create(
            depot=self.depot, activation_date=activation, deactivation_date=deactivation, start_date=TODAY,
            cancellation_date=TODAY - DAY if (cancelled or deactivation) else None)
        part_deactivation = part_deactivation or deactivation
        part_activation = activation if part_activation is True else part_activation
        for category in categories:
            SubscriptionPart.objects.create(
                subscription=sub, type=self.types[category], activation_date=part_activation,
                deactivation_date=part_deactivation, cancellation_date=TODAY - 2 * DAY if part_deactivation or cancelled else None)
        member.join_subscription(sub, True)
        if leave:
            membership = SubscriptionMembership.objects.get(member=member, subscription=sub)
            membership.leave_date = leave
            membership.save()
        return member

    def _result(self, *categories):
        return set(members_with_active_subscription_in_categories(categories))

    def test_nur_gewaehlte_kategorie(self):
        a = self._subscriber('Gemuese', self.gemuese)
        b = self._subscriber('Hof', self.hof)
        self.assertEqual(self._result(self.gemuese), {a})
        self.assertEqual(self._result(self.hof), {b})

    def test_mehrere_kategorien_sind_vereinigung_ohne_doppelte(self):
        both = self._subscriber('Beides', self.gemuese, self.hof)
        a = self._subscriber('Gemuese', self.gemuese)
        self.assertEqual(self._result(self.gemuese, self.hof), {both, a})
        self.assertEqual(members_with_active_subscription_in_categories([self.gemuese, self.hof]).count(), 2)

    def test_gekuendigtes_aber_noch_aktives_abo_zaehlt(self):
        m = self._subscriber('Gekuendigt', self.gemuese, cancelled=True, deactivation=TODAY + DAY)
        self.assertEqual(self._result(self.gemuese), {m})

    def test_wartendes_abo_oder_bestandteil_zaehlt_nicht(self):
        self._subscriber('WartetAbo', self.gemuese, activation=TODAY + DAY, part_activation=TODAY + DAY)
        self._subscriber('WartetTeil', self.hof, part_activation=None)
        self.assertEqual(self._result(self.gemuese, self.hof), set())

    def test_deaktiviertes_abo_zaehlt_nicht(self):
        self._subscriber('AboEnde', self.gemuese, activation=TODAY - 5 * DAY, deactivation=TODAY)
        self.assertEqual(self._result(self.gemuese), set())

    def test_nur_aktiver_bestandteil_der_kategorie(self):
        # Gemüse-Teil beendet, Hofprodukte-Teil aktiv im selben Abo. Der aktive Teil zuerst:
        # juntagrico verlangt für ein nicht gekündigtes Abo mindestens einen aktiven Bestandteil.
        member = self._member('Wechsel')
        sub = Subscription.objects.create(depot=self.depot, activation_date=TODAY - 9 * DAY, start_date=TODAY)
        SubscriptionPart.objects.create(subscription=sub, type=self.types[self.hof], activation_date=TODAY - 9 * DAY)
        SubscriptionPart.objects.create(subscription=sub, type=self.types[self.gemuese],
                                        activation_date=TODAY - 9 * DAY, deactivation_date=TODAY - DAY,
                                        cancellation_date=TODAY - 2 * DAY)
        member.join_subscription(sub, True)
        self.assertEqual(self._result(self.gemuese), set())
        self.assertEqual(self._result(self.hof), {member})

    def test_kategorielose_pakete_gehoeren_zu_keiner_kategorie(self):
        self._subscriber('Ohne', None)
        self.assertEqual(self._result(self.gemuese, self.hof), set())

    def test_ausgetretenes_abo_mitglied_zaehlt_nicht(self):
        self._subscriber('Weg', self.gemuese, leave=TODAY)
        self.assertEqual(self._result(self.gemuese), set())

    def test_deaktiviertes_mitglied_zaehlt_nicht(self):
        m = self._subscriber('Inaktiv', self.gemuese)
        Member.objects.filter(pk=m.pk).update(deactivation_date=TODAY)
        self.assertEqual(self._result(self.gemuese), set())

    def test_formular_zaehlt_empfaenger(self):
        a = self._subscriber('Gemuese', self.gemuese)
        self._subscriber('Hof', self.hof)
        sender = self._member('Sender')
        form = CategoryRecipientsForm(sender, data={'to_categories': [self.gemuese.pk]})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.count_recipients(), 1)
        self.assertEqual(set(form._get_recipients_queryset()), {a})
        self.assertIn('to_categories', form.form_fields)

    def test_formular_kombiniert_mit_kopie(self):
        self._subscriber('Gemuese', self.gemuese)
        sender = self._member('Sender')
        form = CategoryRecipientsForm(sender, data={'to_categories': [self.gemuese.pk], 'copy': 'on'})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.count_recipients(), 2)

    def test_kategoriefeld_fehlt_bei_eingeschraenkter_berechtigung(self):
        sender = self._member('Sender')
        self.assertIn('to_categories', CategoryRecipientsForm(sender).fields)
        restricted = CategoryRecipientsForm(sender, depots=Depot.objects.all())
        self.assertNotIn('to_categories', restricted.fields)
        self.assertNotIn('to_categories', restricted.form_fields)

    def test_audit_protokolliert_kategoriegruppe(self):
        from django.test import RequestFactory
        request = RequestFactory().post('/email/write/', {
            'submit': 'Senden', 'from_email': 'a@b.ch', 'subject': 'S', 'to_categories': ['1']})
        EmailAuditMiddleware(lambda r: None)(request)
        self.assertEqual(EmailAuditLog.objects.get().recipient_groups, 'Abo-BezieherInnen nach Abokategorie')
