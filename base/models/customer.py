from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity


class Customer(AuthBaseEntity):
    class Meta:
        ordering = ['-created', '-modified']

    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    name = models.CharField(max_length=150, unique=True)
    is_credit = models.BooleanField(default=False)
    days_to_clear_invoice = models.IntegerField(default=7)
    physical_address = models.TextField(blank=True, null=True)
    pin_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    vat_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.CharField(max_length=50, unique=True, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}-{self.phone_number}"
