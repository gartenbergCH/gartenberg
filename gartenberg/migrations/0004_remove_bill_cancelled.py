from django.db import migrations
from django.db.migrations.recorder import MigrationRecorder

# Bis v5.1.5 kam juntagrico-billing aus dem Fork-Branch mit PR #78 ("Rechnungen verwerfen").
# Dessen Migration juntagrico_billing.0007_bill_cancelled hat die Spalte Bill.cancelled angelegt.
# Upstream hat PR #78 abgelehnt; mit juntagrico-billing 2.0.1 fehlt das Feld im Modell, die
# Spalte (NOT NULL, ohne DB-Default) liesse jedes Anlegen einer Rechnung scheitern.
#
# Verworfene Rechnungen werden nicht gelöscht, sonst gälten ihre Abo-Teile wieder als
# unverrechnet und "Rechnungen erzeugen" legte sie beim nächsten Lauf neu an. Stattdessen
# bleiben sie mit Betrag 0 als bezahlt stehen; der ursprüngliche Betrag steht in der Notiz.

BILL_TABLE = 'juntagrico_billing_bill'
PAYMENT_TABLE = 'juntagrico_billing_payment'
COLUMN = 'cancelled'
FORK_MIGRATION = '0007_bill_cancelled'
NOTE = 'Verworfen (vor Wechsel auf juntagrico-billing 2.0.1), ursprünglicher Betrag CHF {amount:.2f}.'


def has_cancelled_column(connection):
    with connection.cursor() as cursor:
        columns = connection.introspection.get_table_description(cursor, BILL_TABLE)
    return any(column.name == COLUMN for column in columns)


def remove_cancelled_bills(apps, connection):
    if not has_cancelled_column(connection):
        return []

    qn = connection.ops.quote_name
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT b.id FROM {qn(BILL_TABLE)} b WHERE b.{qn(COLUMN)} '
            f'AND EXISTS (SELECT 1 FROM {qn(PAYMENT_TABLE)} p WHERE p.bill_id = b.id) ORDER BY b.id'
        )
        with_payments = [row[0] for row in cursor.fetchall()]
        if with_payments:
            raise RuntimeError(
                f'Verworfene Rechnungen mit Zahlungen: {with_payments}. '
                'Vor der Migration von Hand bereinigen (Zahlung umbuchen oder Rechnung wiederherstellen).'
            )
        cursor.execute(f'SELECT id FROM {qn(BILL_TABLE)} WHERE {qn(COLUMN)} ORDER BY id')
        cancelled_ids = [row[0] for row in cursor.fetchall()]

    Bill = apps.get_model('juntagrico_billing', 'Bill')
    BillItem = apps.get_model('juntagrico_billing', 'BillItem')
    for bill in Bill.objects.filter(id__in=cancelled_ids):
        note = NOTE.format(amount=bill.amount)
        bill.private_notes = f'{bill.private_notes}\n{note}' if bill.private_notes else note
        # update() statt save(): keine Neuberechnung von Betrag oder MWST über die Modelllogik.
        Bill.objects.filter(id=bill.id).update(amount=0, paid=True, private_notes=bill.private_notes)
    BillItem.objects.filter(bill_id__in=cancelled_ids).update(amount=0, vat_amount=0)

    with connection.cursor() as cursor:
        cursor.execute(f'ALTER TABLE {qn(BILL_TABLE)} DROP COLUMN {qn(COLUMN)}')
    MigrationRecorder(connection).migration_qs.filter(app='juntagrico_billing', name=FORK_MIGRATION).delete()
    return cancelled_ids


def forwards(apps, schema_editor):
    remove_cancelled_bills(apps, schema_editor.connection)


class Migration(migrations.Migration):

    dependencies = [
        ('gartenberg', '0003_seed_subscriptiontypeproductsize'),
        ('juntagrico_billing', '0006_alter_payment_paid_date'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
