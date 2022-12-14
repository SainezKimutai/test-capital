from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity


class Supplier(AuthBaseEntity):
    class Meta:
        ordering = ['-created', '-modified']

    supplier_name = models.CharField(max_length=150, unique=True)
    phone_number_1 = PhoneNumberField(blank=True, null=True)
    phone_number_2 = PhoneNumberField(blank=True, null=True)
    email = models.CharField(max_length=50, unique=True)
    physical_address = models.TextField(blank=True, null=True)
    pin_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    vat_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    contact_person = models.CharField(max_length=150, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.supplier_name}-{self.phone_number_1}"
