from django.db import models

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.category import Category


class Finish(AuthBaseEntity):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='finishCategory')
    name = models.CharField(max_length=70)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
