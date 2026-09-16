from django.db.models.functions import Lower

from juntagrico import defaults


def _product_depotlist_context(product_name):
    """Builds an extra_context function that restricts a depotlist.html export to one product."""
    def extra_context(context):
        from juntagrico.entity.subs import Subscription, SubscriptionPart
        from juntagrico.entity.subtypes import SubscriptionProduct

        from gartenberg.templatetags.gartenberg.depot_extras import ambiguous_types

        products = SubscriptionProduct.objects.filter(name=product_name).on_depot_list()
        # Massgebend ist, ob der Bestandteil des Produkts am Stichtag aktiv ist, nicht das Abo:
        # sonst erscheinen Abos mit nur bestelltem oder bereits deaktiviertem Bestandteil
        # (z.B. ein aktives Gemüse-Abo mit wartendem Mehl) als leere Zeile.
        # Gekündigte, aber noch nicht deaktivierte Bestandteile bleiben aktiv und erscheinen.
        active_parts = SubscriptionPart.objects.filter(
            type__bundle__product_sizes__product__name=product_name,
            type__bundle__product_sizes__show_on_depot_list=True,
        ).active_on(context['date'])
        subscriptions = Subscription.objects.filter(
            id__in=active_parts.values('subscription_id'),
        ).order_by(
            # Subscription hat keine Meta.ordering; ohne dieses order_by kämen die Zeilen in
            # beliebiger DB-Reihenfolge. Gleiche Sortierung wie juntagrico.util.depot_list,
            # dessen Basis-Kontext hier überschrieben wird.
            Lower('primary_member__first_name'), Lower('primary_member__last_name'),
        ).distinct()
        messages = list(context.get('messages', [])) + [
            f'Abo-Typ "{sub_type}" hat keine Produktgrösse auf Depotliste zugeordnet und wird nicht gezählt.'
            for sub_type in ambiguous_types(product_name).filter(subscription_parts__in=active_parts).distinct()
        ]
        return dict(products=products, subscriptions=subscriptions, messages=messages)
    return extra_context


DEPOT_LISTS = defaults.DEPOT_LISTS | {
    # Weiterhin nur Gemüse, damit die Haupt-, Depot- und Mengenübersicht nicht durch
    # die Hofprodukte-Kategorien unübersichtlich werden.
    'depotlist': {
        'template': 'exports/depotlist.html',
        'extra_context': _product_depotlist_context('Gemüse'),
    },
    'depot_overview': {
        'template': 'exports/depot_overview.html',
        'extra_context': _product_depotlist_context('Gemüse'),
    },
    'amount_overview': {
        'template': 'exports/amount_overview.html',
        'extra_context': _product_depotlist_context('Gemüse'),
    },
    'depotlist_kartoffeln': {
        'name': 'Kartoffeln-Liste',
        'template': 'exports/depotlist.html',
        'extra_context': _product_depotlist_context('Kartoffeln'),
    },
    'depotlist_mehl': {
        'name': 'Mehl-Liste',
        # Mehl (10 Produktgrössen) und Glarner Alpkäse (8) sprengen die Portrait-Tabelle;
        # Querformat ohne "abgeholt"/"Tasche retour"-Spalten passt auf die Seite
        # (siehe gartenberg/templates/exports/depotlist_compact.html).
        'template': 'exports/depotlist_compact.html',
        'extra_context': _product_depotlist_context('Mehl'),
    },
    'depotlist_alpkaese': {
        'name': 'Glarner Alpkäse-Liste',
        'template': 'exports/depotlist_compact.html',
        'extra_context': _product_depotlist_context('Glarner Alpkäse'),
    },
}
