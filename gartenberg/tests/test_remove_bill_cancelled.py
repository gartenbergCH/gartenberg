import datetime
from importlib import import_module

from django.apps import apps
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder
from django.test import TestCase
from juntagrico.entity.member import Member
from juntagrico_billing.models.bill import Bill, BillItem, BusinessYear
from juntagrico_billing.models.payment import Payment, PaymentType

migration = import_module('gartenberg.migrations.0004_remove_bill_cancelled')


class RemoveBillCancelledTest(TestCase):
    """Migration 0004: Rückbau von Bill.cancelled aus dem Fork-Branch (abgelehnter PR #78)."""

    @classmethod
    def setUpTestData(cls):
        cls.member = Member.objects.create(
            first_name='Franz', last_name='Muster', email='franz@e2e-test.local',
            addr_street='Teststrasse 1', addr_zipcode='5000', addr_location='Aarau',
            phone='079 111 11 11', confirmed=True, reachable_by_email=False,
        )
        cls.year = BusinessYear.objects.create(
            name='2026', start_date=datetime.date(2026, 1, 1), end_date=datetime.date(2026, 12, 31),
        )

    def make_bill(self, amount, private_notes=None):
        bill = Bill.objects.create(
            business_year=self.year, member=self.member, bill_date=datetime.date(2026, 9, 14),
            booking_date=datetime.date(2026, 9, 14), private_notes=private_notes,
        )
        BillItem.objects.create(bill=bill, description='Gemüse - 1/2 Ernteanteil', amount=amount)
        bill.refresh_from_db()
        return bill

    def add_fork_column(self, cancelled_ids):
        with connection.cursor() as cursor:
            cursor.execute(f'ALTER TABLE {migration.BILL_TABLE} ADD COLUMN cancelled boolean NOT NULL DEFAULT FALSE')
            for bill_id in cancelled_ids:
                cursor.execute(f'UPDATE {migration.BILL_TABLE} SET cancelled = TRUE WHERE id = %s', [bill_id])
        MigrationRecorder(connection).record_applied('juntagrico_billing', migration.FORK_MIGRATION)

    def fork_migration_recorded(self):
        return MigrationRecorder(connection).migration_qs.filter(
            app='juntagrico_billing', name=migration.FORK_MIGRATION).exists()

    def test_ohne_spalte_passiert_nichts(self):
        bill = self.make_bill(234.9)
        self.assertEqual(migration.remove_cancelled_bills(apps, connection), [])
        bill.refresh_from_db()
        self.assertEqual(bill.amount, 234.9)
        self.assertFalse(bill.paid)

    def test_verworfene_rechnungen_auf_null_und_spalte_entfernt(self):
        cancelled = self.make_bill(234.9, private_notes='Wegen Pausierung ausgelöst.')
        cancelled_without_note = self.make_bill(4.3)
        active = self.make_bill(108.65)
        self.add_fork_column([cancelled.id, cancelled_without_note.id])

        result = migration.remove_cancelled_bills(apps, connection)

        self.assertEqual(result, [cancelled.id, cancelled_without_note.id])
        self.assertFalse(migration.has_cancelled_column(connection))
        self.assertFalse(self.fork_migration_recorded())

        cancelled.refresh_from_db()
        self.assertEqual(cancelled.amount, 0)
        self.assertTrue(cancelled.paid)
        self.assertFalse(cancelled.published)
        self.assertEqual(
            cancelled.private_notes,
            'Wegen Pausierung ausgelöst.\n'
            'Verworfen (vor Wechsel auf juntagrico-billing 2.0.1), ursprünglicher Betrag CHF 234.90.',
        )
        # Die Position bleibt bestehen, damit der Abo-Teil weiterhin als verrechnet gilt.
        item = cancelled.items.get()
        self.assertEqual((item.amount, item.vat_amount), (0, 0))

        cancelled_without_note.refresh_from_db()
        self.assertEqual(
            cancelled_without_note.private_notes,
            'Verworfen (vor Wechsel auf juntagrico-billing 2.0.1), ursprünglicher Betrag CHF 4.30.',
        )

        active.refresh_from_db()
        self.assertEqual(active.amount, 108.65)
        self.assertFalse(active.paid)
        self.assertIsNone(active.private_notes)

        # Ohne Spalte lässt sich wieder eine Rechnung anlegen.
        self.make_bill(50)

    def test_bricht_bei_verworfener_rechnung_mit_zahlung_ab(self):
        bill = self.make_bill(155.75)
        payment_type = PaymentType.objects.create(name='Bank', iban='CH00', booking_account='1010')
        Payment.objects.create(bill=bill, type=payment_type, paid_date=datetime.date(2026, 9, 20), amount=10)
        self.add_fork_column([bill.id])

        with self.assertRaisesMessage(RuntimeError, f'[{bill.id}]'):
            migration.remove_cancelled_bills(apps, connection)
        self.assertTrue(migration.has_cancelled_column(connection))
