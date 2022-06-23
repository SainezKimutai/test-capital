from django.db import models

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.inventory import Inventory


class Promotion(AuthBaseEntity):
    class Meta:
        ordering = ['-created', '-modified']

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    promotion_price = models.IntegerField(default=0)
    promotion_start_date = models.DateField(null=False, blank=False)
    promotion_end_date = models.DateField(null=False, blank=False)
    description = models.CharField(max_length=250)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.inventory.name}"
