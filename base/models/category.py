from django.db import models
from django.db.models.deletion import PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity


class Category(AuthBaseEntity):
    name = models.CharField(max_length=90, unique=True)
    parent = models.ForeignKey('self', on_delete=PROTECT, blank=True, null=True, related_name='sub_category')
    category_image = models.ImageField(upload_to='category/%Y/%m/%d', null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def get_children(self):
        return Category.objects.filter(parent=self)
