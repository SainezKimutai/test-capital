from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import PROTECT

from extended_choices.choices import Choices
from multiselectfield import MultiSelectField
from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.sales import SalesOrder


class Invoice(AuthBaseEntity):
    class Meta:
        ordering = ['-created', '-modified']

    TRANSACTION_TYPE = Choices(
        ['CASH', 'CASH', 'CASH'],
        ['MPESA', 'MPESA', 'MPESA']
    )

    PAYMENT_STATUS = Choices(
        ['PARTIALLY_PAID', 'PARTIALLY_PAID', 'PARTIALLY_PAID'],
        ['FULLY_PAID', 'FULLY_PAID', 'FULLY_PAID'],
        ['NOT_PAID', 'NOT_PAID', 'NOT_PAID']
    )

    sales_order = models.ForeignKey(SalesOrder, blank=False, on_delete=PROTECT)
    expected_payment_date = models.DateField(null=False, blank=False)
    payment_date = models.DateField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=20, blank=True, null=True)
    transaction_type = MultiSelectField(max_length=40, choices=TRANSACTION_TYPE, blank=True, null=True)
    cash_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    pending_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    mpesa_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
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
