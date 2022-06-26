from django.db import models
from django.db.models.deletion import CASCADE, PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.inventory import Inventory
from base.models.supplier import Supplier


class Replenishment(AuthBaseEntity):

    class Meta:
        ordering = ['-modified', '-created']

    supplier = models.ForeignKey(Supplier, on_delete=PROTECT)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=500, null=False, blank=False)
    delivery_number = models.CharField(max_length=500, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.receipt_number}"

    @property
    def items(self):
        return ReplenishmentItem.objects.filter(replenishment=self)


class ReplenishmentItem(AuthBaseEntity):
    
    class Meta:
        ordering = ['-created', '-modified']

    replenishment = models.ForeignKey(Replenishment, on_delete=CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=CASCADE)
    count = models.IntegerField(null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.inventory.name}"
