"""Ersetzt die juntagrico-Library 'juntagrico.depot_extras' (siehe TEMPLATES in settings.py).

Alle Filter und Tags werden unverändert übernommen, nur parts_by_size berücksichtigt die
Zuordnung Abo-Typ → Produktgrösse (UC-004 GR-008). Über die Library statt über eigene
Template-Kopien, damit auch die unveränderten juntagrico-Templates (Kartoffeln-Liste,
Depot- und Mengenübersicht) korrekt zählen.
"""
from django import template
from django.db.models import Count, Q

from juntagrico.entity.subtypes import SubscriptionType
from juntagrico.templatetags.juntagrico import depot_extras as juntagrico_depot_extras

register = template.Library()
register.tags.update(juntagrico_depot_extras.register.tags)
register.filters.update(juntagrico_depot_extras.register.filters)


def ambiguous_types(product_name):
    """Abo-Typen ohne Zuordnung, deren Paket mehrere Grössen des Produkts enthält."""
    return SubscriptionType.objects.filter(depot_list_product_size__isnull=True).annotate(
        product_size_count=Count(
            'bundle__product_sizes', filter=Q(bundle__product_sizes__product__name=product_name), distinct=True,
        ),
    ).filter(product_size_count__gt=1)


@register.filter
def parts_by_size(subscriptions, product_size):
    parts = juntagrico_depot_extras.parts_by_size(subscriptions, product_size)
    # Zugeordnete Typen zählen nur in ihrer Grösse. Nicht zugeordnete zählen wie in juntagrico
    # in jeder Grösse ihres Pakets, ausser das Paket enthält mehrere Grössen dieses Produkts:
    # dann ist die Grösse unbekannt, und die Liste weist einen Hinweis aus statt falsch zu zählen.
    return parts.filter(
        Q(type__depot_list_product_size__product_size=product_size)
        | (
            Q(type__depot_list_product_size__isnull=True)
            & ~Q(type__in=ambiguous_types(product_size.product.name).values('pk'))
        )
    )
