from django.contrib import admin

from .models import EmailAuditLog


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
