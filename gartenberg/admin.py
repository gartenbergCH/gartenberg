from django.contrib import admin

from juntagrico.entity.subtypes import SubscriptionType
from juntagrico.util import addons

from .models import EmailAuditLog, SubscriptionTypeProductSize


class SubscriptionTypeProductSizeInline(admin.TabularInline):
    model = SubscriptionTypeProductSize
    extra = 0
    max_num = 1


# Wie juntagrico-billing: Inline am juntagrico-Admin des Abo-Typs anhängen, statt
# dessen ModelAdmin neu zu registrieren. Funktioniert, weil 'gartenberg' in
# INSTALLED_APPS vor 'juntagrico' steht und dieses Modul daher früher geladen wird.
addons.config.register_model_inline(SubscriptionType, SubscriptionTypeProductSizeInline)


@admin.register(EmailAuditLog)
class EmailAuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'sender', 'subject', 'recipient_groups', 'url')
    list_filter = ('sender', 'url')
    search_fields = ('sender', 'subject')
    readonly_fields = ('timestamp', 'sender', 'subject', 'recipient_groups', 'url')
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
