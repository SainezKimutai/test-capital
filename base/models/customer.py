from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity


class Customer(AuthBaseEntity):
    phone_number = PhoneNumberField(blank=False, null=False, unique=True)
    name = models.CharField(max_length=150, unique=True)
    is_credit = models.BooleanField(default=False)
    days_to_clear_invoice = models.IntegerField(default=7)
    physical_address = models.TextField(blank=True)
    pin_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    vat_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.CharField(max_length=50, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}-{self.phone_number}"
