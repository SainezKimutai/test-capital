from django.db import models
from django.db.models.deletion import PROTECT

from extended_choices.choices import Choices
from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.category import Category


class Size(AuthBaseEntity):
    SIZE_TYPE = Choices(
        ['LITRES', 'LITRES', 'LITRES'],
        ['METERS', 'METERS', 'METERS'],
        ['CENTIMETERS', 'CENTIMETERS', 'CENTIMETERS'],
        ['KGS', 'KGS', 'KGS'],
        ['GRAMS', 'GRAMS', 'GRAMS'],
        ['ROLLS', 'ROLLS', 'ROLLS'],
        ['FEET', 'FEET', 'FEET'],
        ['INCHES', 'INCHES', 'INCHES'],
    )

    category = models.ForeignKey(Category, on_delete=PROTECT, related_name='sizeCategory')
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE, blank=False, null=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.value}-{self.size_type}-{self.category.name}"
