from django.core.exceptions import ValidationError
from django.db import models

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.sales import SalesOrder


class Invoice(AuthBaseEntity):
    sales_order = models.ForeignKey(SalesOrder, blank=False,)
    expected_payment_date = models.DateField(null=False, blank=False)
    payment_date = models.DateField(null=True, blank=False)
    paid = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.sales_order}"

    def clean(self):
        # Ensure all sales items are from the same order
        if self.paid and not self.payment_date:
            raise ValidationError(
                {'paid': "Invoice cannot be marked as paid without a payment date"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
