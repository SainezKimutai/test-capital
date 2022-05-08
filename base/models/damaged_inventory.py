from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.inventory import Inventory
from base.models.supplier import Supplier


class DamagedInventory(AuthBaseEntity):
    inventory = models.ForeignKey(Inventory, on_delete=PROTECT)
    count = models.IntegerField(null=False, blank=False)
    damage_reason = models.CharField(max_length=250)
    quantity_before = models.IntegerField(null=False, blank=False)
    quantity_after = models.IntegerField(null=False, blank=False)
    replaceable = models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier, on_delete=PROTECT)
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        null=False,
        blank=False,
        default=None,
        editable=False,
        related_name="damaged_by_%(app_label)s_%(class)s_set",
        verbose_name="damaged by")
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.inventory.name}"

    def clean(self):
        if self.replaceable and not self.supplier:
            raise ValidationError(
                {'supplier': "Supplier cannot be empty if the damaged stock is replaceable."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
