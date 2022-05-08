from django.db import models
from django.db.models.deletion import PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.inventory import Inventory
from base.models.supplier import Supplier


class Replenishment(AuthBaseEntity):
    inventory = models.ForeignKey(Inventory, on_delete=PROTECT)
    count = models.IntegerField(null=False, blank=False)
    supplier = models.ForeignKey(Supplier, on_delete=PROTECT)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=50, null=False, blank=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.inventory.name}"
