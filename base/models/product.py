from django.db import models
from django.db.models.deletion import PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.category import Category


class Product(AuthBaseEntity):
    title = models.CharField(max_length=180)
    description = models.TextField()
    product_category = models.ForeignKey(Category, on_delete=PROTECT, related_name='product')
    price = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to='product')
    history = HistoricalRecords()

    def __str__(self):
        return self.title
