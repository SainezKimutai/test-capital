from django.db import models

from base.models.base import AuthBaseEntity
from base.models.product import Product
from simple_history.models import HistoricalRecords


class Cart(AuthBaseEntity):
    products = models.ManyToManyField(Product, null=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.total
