from django.db import models

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
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sizeCategory')
    name = models.CharField(max_length=70)
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE, blank=False, null=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
