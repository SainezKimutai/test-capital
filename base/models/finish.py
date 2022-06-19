from django.db import models
from django.db.models.deletion import PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.category import Category


class Finish(AuthBaseEntity):
    class Meta:
        ordering = ['-created', '-modified']

    category = models.ForeignKey(Category, on_delete=PROTECT, related_name='finishCategory')
    name = models.CharField(max_length=70)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}-{self.category.name}"
