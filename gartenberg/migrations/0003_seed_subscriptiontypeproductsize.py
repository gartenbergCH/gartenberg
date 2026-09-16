from django.db import migrations

# Stand der Abo-Typen vom 16.09.2026 (UC-004 GR-008). Pakete "Mehl" und "Glarner Alpkäse"
# enthalten alle Grössen ihres Produkts; die bestellte Grösse steckt nur im Typ-Namen.
# Neue oder umbenannte Typen werden im Admin beim Abo-Typ zugeordnet.
MAPPING = {
    'Mehl': {
        'Weizenmehl Halbweiss 1kg': 'Weizen HW 1kg',
        'Weizenmehl Halbweiss 3kg': 'Weizen HW 3kg',
        'Weizenmehl Ruch 1kg': 'Weizen Ruch 1kg',
        'Weizenmehl Ruch 3kg': 'Weizen Ruch 3kg',
        'Weizenmehl Vollkorn 1kg': 'Weizen Voll 1kg',
        'Weizenmehl Vollkorn 3kg': 'Weizen Voll 3kg',
        'Dinkelmehl Halbweiss 1kg': 'Dinkel HW 1kg',
        'Dinkelmehl Halbweiss 3kg': 'Dinkel HW 3kg',
        'Dinkelmehl Ruch 1kg': 'Dinkel Ruch 1kg',
        'Dinkelmehl Ruch 3kg': 'Dinkel Ruch 3kg',
    },
    'Glarner Alpkäse': {
        'AOP Bio ca. 300g': 'AOP Bio 300g',
        'AOP Bio ca.1kg': 'AOP Bio 1kg',
        'AOP gereift Bio ca.300g': 'AOP 1 Jahr 300g',
        'AOP gereift Bio ca. 1kg': 'AOP 1 Jahr 1kg',
        'Kräuter (konventionell) ca.300g': 'Kräuter 300g',
        'Kräuter (konventionell) ca.1kg': 'Kräuter 1kg',
        'Nidel Bio ca.300g': 'Nidel 300g',
        'Nidel Bio ca.1kg': 'Nidel 1kg',
    },
}


def seed(apps, schema_editor):
    SubscriptionType = apps.get_model('juntagrico', 'SubscriptionType')
    ProductSize = apps.get_model('juntagrico', 'ProductSize')
    SubscriptionTypeProductSize = apps.get_model('gartenberg', 'SubscriptionTypeProductSize')
    for product_name, sizes_by_type in MAPPING.items():
        for type_name, size_name in sizes_by_type.items():
            # Nur zuordnen, was in dieser Datenbank so existiert (Test-/Staging-Systeme
            # haben andere oder keine Hofprodukte) und die Grösse im Paket des Typs enthält.
            size = ProductSize.objects.filter(product__name=product_name, name=size_name).first()
            if size is None:
                continue
            for sub_type in SubscriptionType.objects.filter(name=type_name, bundle__product_sizes=size).distinct():
                SubscriptionTypeProductSize.objects.get_or_create(
                    subscription_type=sub_type, defaults={'product_size': size},
                )


class Migration(migrations.Migration):

    dependencies = [
        ('gartenberg', '0002_subscriptiontypeproductsize'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
