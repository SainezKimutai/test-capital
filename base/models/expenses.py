from django.conf import settings
from django.db import models
from django.db.models.deletion import PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity


class Expense(AuthBaseEntity):
    description = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        null=False,
        blank=False,
        default=None,
        editable=False,
        related_name="expense_by_%(app_label)s_%(class)s_set",
        verbose_name="expense by")
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.inventory.name}"
