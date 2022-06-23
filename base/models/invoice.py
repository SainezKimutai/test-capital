from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.sales import SalesOrder


class Invoice(AuthBaseEntity):
    class Meta:
        ordering = ['-created', '-modified']

    sales_order = models.ForeignKey(SalesOrder, blank=False, on_delete=PROTECT)
    expected_payment_date = models.DateField(null=False, blank=False)
    payment_date = models.DateField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.sales_order}"

    @property
    def is_past_due(self):
        if self.paid:
            if self.expected_payment_date > self.payment_date:
                return "Paid on Time"
            else:
                return "Paid late"
        return date.today() > self.expected_payment_date

    def clean(self):
        # Ensure all sales items are from the same order
        if self.paid and not self.payment_date:
            raise ValidationError(
                {'paid': "Invoice cannot be marked as paid without a payment date"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
