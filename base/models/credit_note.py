from django.db.models.deletion import PROTECT
from django.db import models

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.sales import SalesItem


class CreditNote(AuthBaseEntity):
    sales_item = models.ForeignKey(
        SalesItem,
        blank=False,
        on_delete=PROTECT
    )
    credit_note_reason = models.CharField(max_length=250, null=False, blank=False)
    affects_cash = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.id}"
