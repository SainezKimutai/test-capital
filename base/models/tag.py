from django.db import models

from base.models.base import AuthBaseEntity
from simple_history.models import HistoricalRecords


class Tag(AuthBaseEntity):
    name = models.CharField(max_length=70)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
