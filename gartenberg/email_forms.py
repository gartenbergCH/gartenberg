"""Rundmail an Abo-BezieherInnen einer Abokategorie (UC-005, FR-057).

juntagrico kennt im Formular unter /email/write/ nur "alle mit aktivem Abo" oder einzelne
Depots. GartenBerg unterscheidet die Kategorien Gemüse und Hofprodukte und will gezielt
nur eine davon anschreiben. Die Erweiterung erfolgt hier, ohne juntagrico zu ändern.
"""
import datetime

from django import forms
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_select2.forms import Select2MultipleWidget

from juntagrico.config import Config
from juntagrico.entity.member import Member, SubscriptionMembership
from juntagrico.entity.subs import Subscription, SubscriptionPart
from juntagrico.entity.subtypes import SubscriptionCategory
from juntagrico.forms.email import EmailForm, RecipientsForm


def members_with_active_subscription_in_categories(categories, on_date=None):
    """Aktive Mitglieder mit aktivem Abo, das einen aktiven Bestandteil aus einer der Kategorien hat.

    UC-005 GR-007. Ein gekündigtes Abo zählt bis zu seiner Deaktivierung, ein wartendes
    Abo bzw. ein wartender Bestandteil (noch nicht aktiviert) zählt nicht.
    """
    on_date = on_date or datetime.date.today()
    parts = SubscriptionPart.objects.filter(
        Q(deactivation_date__isnull=True) | Q(deactivation_date__gt=on_date),
        activation_date__isnull=False, activation_date__lte=on_date,
        type__bundle__category__in=categories,
    )
    subscriptions = Subscription.objects.active(on_date).filter(
        Q(deactivation_date__isnull=True) | Q(deactivation_date__gt=on_date),
        pk__in=parts.values('subscription'),
    )
    memberships = SubscriptionMembership.objects.filter(
        Q(leave_date__isnull=True) | Q(leave_date__gt=on_date),
        join_date__isnull=False, join_date__lte=on_date,
        subscription__in=subscriptions,
    )
    return Member.objects.active(on_date).filter(pk__in=memberships.values('member'))


class CategoryRecipientsForm(RecipientsForm):
    to_categories = forms.ModelMultipleChoiceField(
        SubscriptionCategory.objects.order_by('sort_order'),
        label=_('An alle mit aktivem/r {} in diesen Kategorien').format(Config.vocabulary('subscription')),
        required=False,
        widget=Select2MultipleWidget(attrs={'data-minimum-input-length': 0}),
    )

    form_fields = ['to_list', 'to_categories', 'to_areas', 'to_jobs', 'to_depots', 'to_members', 'copy']

    def __init__(self, sender, *args, areas=None, depots=None, **kwargs):
        super().__init__(sender, *args, areas=areas, depots=depots, **kwargs)
        # Wie bei "alle mit Abo" nur für Personen mit allgemeinem Versandrecht: wer nur auf
        # eigene Depots/Tätigkeitsbereiche beschränkt ist, darf nicht alle einer Kategorie anschreiben.
        if (areas is not None or depots is not None) and 'to_categories' in self.fields:
            del self.fields['to_categories']
            self.form_fields.remove('to_categories')

    def get_count_url(self):
        return reverse('gartenberg-email-count-recipients')

    def _populate_recipients_queryset(self, recipients):
        if to_categories := self.cleaned_data.get('to_categories'):
            recipients |= members_with_active_subscription_in_categories(to_categories)
        return super()._populate_recipients_queryset(recipients)


class CategoryEmailForm(EmailForm, CategoryRecipientsForm):
    pass
