from django.db import migrations


# UC-001 GR-007: Die Beitrittserklärung ist nur bei regulären Abos Pflicht. juntagrico legt
# SubscriptionType.requires_membership standardmässig auf True; Probe-Abo-Typen erkennt man an
# ihrer Probedauer. Später erfasste Probe-Typen werden im Admin entsprechend eingestellt.
def trial_types_without_membership(apps, schema_editor):
    SubscriptionType = apps.get_model('juntagrico', 'SubscriptionType')
    SubscriptionType.objects.filter(trial_days__gt=0).update(requires_membership=False)


class Migration(migrations.Migration):

    dependencies = [
        ('gartenberg', '0004_remove_bill_cancelled'),
        ('juntagrico', '0064_alter_specialroles_options'),
    ]

    operations = [
        migrations.RunPython(trial_types_without_membership, migrations.RunPython.noop),
    ]
