import uuid

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.db.models.deletion import PROTECT

from extended_choices.choices import Choices
from multiselectfield import MultiSelectField
from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.customer import Customer
from base.models.inventory import Inventory


class SalesOrder(AuthBaseEntity):
    class Meta:
        ordering = ['-created', '-modified']

    TRANSACTION_TYPE = Choices(
        ['CASH', 'CASH', 'CASH'],
        ['MPESA', 'MPESA', 'MPESA'],
        ['CREDIT', 'CREDIT', 'CREDIT'],
    )

    customer = models.ForeignKey(Customer, on_delete=PROTECT, blank=True, null=True)
    sales_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        null=False,
        blank=False,
        default=None,
        editable=True,
        related_name="sold_by_%(app_label)s_%(class)s_set",
        verbose_name="sold by")
    receipt_number = models.CharField(default=uuid.uuid4, editable=False, null=False, blank=False, max_length=100)
    transaction_type = MultiSelectField(max_length=40, choices=TRANSACTION_TYPE, blank=False, null=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    cash_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    mpesa_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.receipt_number}"


class SalesItem(AuthBaseEntity):
    class Meta:
        ordering = ['-created', '-modified']

    sales_order = models.ForeignKey(SalesOrder, on_delete=PROTECT)
    inventory = models.ForeignKey(Inventory, on_delete=PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.inventory.name}-{self.sales_order.receipt_number}"

    def fully_credited(self):
        """
        Returns True or False
        Check if a certain sale item can be raised as a credit note
        :return:
        """
        from base.models.credit_note import CreditNote
        previous_quantity = CreditNote.objects.filter(sales_item__id=self.id)
        if previous_quantity:
            count = previous_quantity.aggregate(Sum('quantity')).get('quantity__sum')

            if count >= self.quantity:
                return True

        return False
