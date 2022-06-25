from django.conf import settings
from django.db import models
from django.db.models.deletion import PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.inventory import Inventory
from base.models.supplier import Supplier


class DamagedInventory(AuthBaseEntity):

    class Meta:
        ordering = ['-modified', '-created']

    inventory = models.ForeignKey(Inventory, on_delete=PROTECT)
    count = models.IntegerField(null=False, blank=False)
    damage_reason = models.CharField(max_length=250)
    quantity_before = models.IntegerField(null=False, blank=False)
    quantity_after = models.IntegerField(null=False, blank=False)
    replaceable = models.BooleanField(default=False)
    replaced = models.BooleanField(default=False)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=PROTECT,
        null=True,
        blank=True,
        default=None
    )
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        null=True,
        blank=True,
        default=None,
        related_name="damaged_by_%(app_label)s_%(class)s_set",
        verbose_name="damaged by")
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.inventory.name}"
