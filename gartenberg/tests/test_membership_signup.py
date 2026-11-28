from importlib import import_module

from django.apps import apps
from django.test import TestCase
from juntagrico.config import Config
from juntagrico.entity.subtypes import SubscriptionBundle, SubscriptionType

migration = import_module('gartenberg.migrations.0005_trial_types_without_membership')


class MembershipSignupTest(TestCase):
    """UC-001 GR-002 / GR-007: Beitrittserklärung im Anmeldeprozess (seit juntagrico 2.1)."""

    def test_beitrittserklaerung_ohne_anteilschein_und_jahresbeitrag(self):
        self.assertTrue(Config.membership('enable'))
        self.assertEqual(Config.membership('required_shares'), 0)
        self.assertEqual(Config.membership('fee'), 0)

    def test_probe_typen_ohne_pflicht_zur_beitrittserklaerung(self):
        bundle = SubscriptionBundle.objects.create(long_name='Gemüse')
        regular = SubscriptionType.objects.create(name='Ganz', bundle=bundle, price=1, required_assignments=0)
        trial = SubscriptionType.objects.create(name='Probe ganz', bundle=bundle, price=1, required_assignments=0, trial_days=90)
        SubscriptionType.objects.update(requires_membership=True)

        migration.trial_types_without_membership(apps, None)

        regular.refresh_from_db()
        trial.refresh_from_db()
        self.assertTrue(regular.requires_membership)
        self.assertFalse(trial.requires_membership)
