from django.db import models


class EmailAuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=254)
    subject = models.CharField(max_length=500)
    recipient_groups = models.CharField(max_length=500)
    url = models.CharField(max_length=200)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.timestamp:%Y-%m-%d %H:%M} | {self.sender} | {self.subject}'
