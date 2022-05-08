import uuid

from django.conf import settings
from django.db import models
from django.db.models.deletion import PROTECT

from extended_choices.choices import Choices
from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.customer import Customer
from base.models.inventory import Inventory


class SalesOrder(AuthBaseEntity):
    TRANSACTION_TYPE = Choices(
        ['CASH', 'CASH', 'CASH'],
        ['MPESA', 'MPESA', 'MPESA'],
        ['CREDIT', 'CREDIT', 'CREDIT'],
    )

    customer = models.ForeignKey(Customer, on_delete=PROTECT)
    sales_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        null=False,
        blank=False,
        default=None,
        editable=False,
        related_name="sold_by_%(app_label)s_%(class)s_set",
        verbose_name="sold by")
    receipt_number = models.CharField(default=uuid.uuid4, editable=False, null=False, blank=False, max_length=100)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE, blank=False, null=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.receipt_number}"


class SalesItem(AuthBaseEntity):
    sales_order = models.ForeignKey(SalesOrder, on_delete=PROTECT)
    inventory = models.ForeignKey(Inventory, on_delete=PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.sales_order.receipt_number}"
