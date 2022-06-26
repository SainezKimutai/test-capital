from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import PROTECT

from simple_history.models import HistoricalRecords

from base.models.base import AuthBaseEntity
from base.models.category import Category
from base.models.color import Color
from base.models.finish import Finish
from base.models.range import Range
from base.models.size import Size
from base.models.tag import Tag


class Inventory(AuthBaseEntity):

    class Meta:
        ordering = ['-modified', '-created']

    name = models.CharField(max_length=120)
    range = models.ForeignKey(Range, on_delete=PROTECT, related_name='productRange')
    category = models.ForeignKey(Category, on_delete=PROTECT, related_name='productCategory')
    short_description = models.CharField(max_length=250)
    full_description = models.TextField()
    color = models.ForeignKey(Color, on_delete=PROTECT, related_name='productColor')
    finish = models.ForeignKey(Finish, on_delete=PROTECT, related_name='productFinish')
    size = models.ForeignKey(Size, on_delete=PROTECT, related_name='productSize')
    reorder_level = models.IntegerField(default=0)
    current_stock = models.IntegerField(default=0)
    stock_unit = models.CharField(max_length=120, default='Packages')
    recent_buying_price = models.IntegerField(default=0, blank=True)
    selling_price = models.IntegerField(default=0)
    max_selling_price = models.IntegerField(default=0)
    min_selling_price = models.IntegerField(default=0)
    wholesale_price = models.IntegerField(default=0)
    wholesale_minimum_number = models.IntegerField(default=0)
    inventory_code = models.CharField(max_length=20, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='inventory_tag')
    picture = models.ImageField(upload_to='inventory/%Y/%m/%d', null=True, blank=True)
    is_deactivated = models.BooleanField(default=False)
    deactivation_reason = models.CharField(max_length=250, blank=True, null=True)
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

        if self.min_selling_price > self.max_selling_price:
            raise ValidationError(
                {'min_selling_price': "Minimum selling price cannot be greater than maximum selling price."})

        if self.selling_price > self.max_selling_price or self.selling_price < self.min_selling_price:
            raise ValidationError(
                {'selling_price': "Selling price should be within minimum and maximum selling ranges"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
