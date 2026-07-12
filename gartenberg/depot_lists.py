from juntagrico import defaults


def _product_depotlist_context(product_name):
    """Builds an extra_context function that restricts a depotlist.html export to one product."""
    def extra_context(context):
        from juntagrico.entity.subs import Subscription
        from juntagrico.entity.subtypes import SubscriptionProduct

        products = SubscriptionProduct.objects.filter(name=product_name).on_depot_list()
        subscriptions = Subscription.objects.filter(
            parts__type__bundle__product_sizes__product__name=product_name,
            parts__type__bundle__product_sizes__show_on_depot_list=True,
        ).active_on(context['date']).distinct()
        return dict(products=products, subscriptions=subscriptions)
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
