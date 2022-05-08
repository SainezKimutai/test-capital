from django.core.exceptions import ValidationError
from django.db import models

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.sales import SalesItem


class CreditNote(AuthBaseEntity):
    sales_item = models.ManyToManyField(
        SalesItem,
        blank=False,
        verbose_name="credit note items",
        related_name="credit_note_items"
    )
    credit_note_reason = models.CharField(max_length=250, null=False, blank=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.id}"

    def clean(self):
        # Ensure all sales items are from the same order
        if len(set(self.sales_item.all().value_list('receipt_number', flat=True))) > 1:
            raise ValidationError(
                {'sales_item': "Credit note items can only be from the same order"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
