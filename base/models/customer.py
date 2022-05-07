from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity


class Customer(AuthBaseEntity):
    phone_number = PhoneNumberField(blank=False, null=False, unique=True)
    name = models.CharField(max_length=150, unique=True)
    is_credit = models.BooleanField(default=True)
    physical_address = models.TextField(blank=True)
    pin_number = models.CharField(max_length=50, unique=True)
    vat_number = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}-{self.phone_number}"
