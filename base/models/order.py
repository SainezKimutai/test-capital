from django.db import models
from django.db.models.deletion import PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.product import Product


# order by user
class Order(AuthBaseEntity):
    full_name = models.CharField(max_length=60, blank=True, null=True)
    phn_number = models.CharField(max_length=14, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.id} {self.full_name}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


# order Item list
class OrderItem(AuthBaseEntity):
    orderItem = models.ForeignKey(Order, related_name='items', on_delete=PROTECT)
    products = models.ForeignKey(Product, related_name='order_items', on_delete=PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity
