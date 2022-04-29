from django.core.exceptions import ValidationError
from django.db import models

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.category import Category
from base.models.color import Color
from base.models.finish import Finish
from base.models.range import Range
from base.models.size import Size
from base.models.tag import Tag


class Inventory(AuthBaseEntity):
    name = models.CharField(max_length=120)
    range = models.ForeignKey(Range, on_delete=models.CASCADE, related_name='productRange')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='productCategory')
    short_description = models.CharField(max_length=250)
    full_description = models.TextField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='productColor')
    finish = models.ForeignKey(Finish, on_delete=models.CASCADE, related_name='productFinish')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='productSize')
    reorder_level = models.IntegerField(default=0)
    current_stock = models.IntegerField(default=0)
    recent_purchase_price = models.IntegerField(default=0)
    selling_price = models.IntegerField(default=0)
    promotional_price = models.IntegerField(default=0)
    wholesale_price = models.IntegerField(default=0)
    wholesale_minimum_number = models.IntegerField(default=0)
    inventory_code = models.CharField(max_length=20, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='inventory_tag')
    picture = models.ImageField(upload_to='inventory/%Y/%m/%d', null=True, blank=True)
    is_promotion = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def clean(self):
        if self.color.category != self.category:
            raise ValidationError(
                {'color': "Color category does not match chosen category."})

        if self.finish.category != self.category:
            raise ValidationError(
                {'finish': "Finish category does not match chosen category."})

        if self.size.category != self.category:
            raise ValidationError(
                {'size': "Size category does not match chosen category."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
