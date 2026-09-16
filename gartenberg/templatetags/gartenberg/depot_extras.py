"""Ersetzt die juntagrico-Library 'juntagrico.depot_extras' (siehe TEMPLATES in settings.py).

Alle Filter und Tags werden übernommen. Angepasst sind parts_by_size, das die Zuordnung
Abo-Typ → Produktgrösse berücksichtigt (UC-004 GR-008), und count_units, das nur die
Einheiten des Hauptprodukts zählt (UC-004 GR-002). Über die Library statt über eigene
Template-Kopien, damit auch die unveränderten juntagrico-Templates (Kartoffeln-Liste,
Depot- und Mengenübersicht) korrekt zählen.
"""
from django import template
from django.db.models import Count, Q, QuerySet

from juntagrico.entity.subs import Subscription
from juntagrico.entity.subtypes import ProductSize, SubscriptionType
from juntagrico.templatetags.juntagrico import depot_extras as juntagrico_depot_extras

from gartenberg.depot_lists import MAIN_PRODUCT_NAME

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


@register.filter
def count_units(subs, date=None):
    """Einheiten-Spalte der Depot- und Mengenübersicht.

    juntagrico summiert die Einheiten aller Produktgrössen im Paket jedes aktiven Bestandteils,
    auch der Hofprodukte. Ein Mehl-Bestandteil zählte so 10 Einheiten (eine je Mehl-Grösse im
    Paket) und blähte das Gemüse-Total auf. Gezählt wird darum nur das Hauptprodukt, und zwar
    wie in den Grössen-Spalten: Einheiten der Grösse × Anzahl Bestandteile dieser Grösse.
    """
    if not isinstance(subs, Subscription) and not (isinstance(subs, QuerySet) and subs.model is Subscription):
        return 0.0
    sizes = ProductSize.objects.filter(product__name=MAIN_PRODUCT_NAME).on_depot_list()
    return float(sum(size.units * parts_by_size(subs, size).active_on(date).count() for size in sizes))
