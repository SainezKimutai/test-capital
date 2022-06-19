from django.db import models

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity


class Tag(AuthBaseEntity):
    class Meta:
        ordering = ['-created', '-modified']

    name = models.CharField(max_length=70)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
