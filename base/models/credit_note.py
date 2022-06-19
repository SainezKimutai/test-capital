from django.db import models
from django.db.models.deletion import PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity


class CreditNote(AuthBaseEntity):
    from base.models.sales import SalesItem

    class Meta:
        ordering = ['-created', '-modified']

    sales_item = models.ForeignKey(
        SalesItem,
        blank=True,
        null=True,
        on_delete=PROTECT
    )
    quantity = models.IntegerField(default=0)
    credit_note_reason = models.CharField(max_length=250, null=False, blank=False)
    affects_cash = models.BooleanField(null=False, blank=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.id}"
