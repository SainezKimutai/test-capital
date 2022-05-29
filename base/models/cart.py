from django.db import models

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.inventory import Inventory


class Cart(AuthBaseEntity):
    inventories = models.ManyToManyField(Inventory, null=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.total
