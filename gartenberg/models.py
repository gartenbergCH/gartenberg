from django.core.exceptions import ObjectDoesNotExist, ValidationError
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


class SubscriptionTypeProductSize(models.Model):
    """Produktgrösse, die ein Abo-Typ auf den Depotlisten bezieht (UC-004 GR-008).

    juntagrico zählt einen Bestandteil in jeder Produktgrösse seines Abo-Pakets. Die Pakete
    "Mehl" und "Glarner Alpkäse" enthalten alle Grössen, die bestellte Grösse steckt nur im
    Abo-Typ. Pro Grösse ein eigenes Paket anzulegen, würde im Bestellformular die
    Paket-Überschriften ausblenden; darum wird die Grösse hier je Typ zugeordnet.
    """
    subscription_type = models.OneToOneField(
        'juntagrico.SubscriptionType', on_delete=models.CASCADE, related_name='depot_list_product_size',
        verbose_name='Abo-Typ',
    )
    product_size = models.ForeignKey(
        'juntagrico.ProductSize', on_delete=models.CASCADE, related_name='+', verbose_name='Produktgrösse',
    )

    class Meta:
        verbose_name = 'Produktgrösse auf Depotliste'
        verbose_name_plural = 'Produktgrösse auf Depotliste'

    def __str__(self):
        return f'{self.subscription_type} → {self.product_size}'

    def clean(self):
        try:
            bundle = self.subscription_type.bundle
        except ObjectDoesNotExist:
            return  # Abo-Typ bzw. Paket noch nicht gesetzt; das meldet dessen eigenes Formular
        if not bundle.product_sizes.filter(pk=self.product_size_id).exists():
            raise ValidationError(
                {'product_size': f'Die Produktgrösse ist nicht im Abo-Paket "{bundle.long_name}" enthalten.'}
            )
