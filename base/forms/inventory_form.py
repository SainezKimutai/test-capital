from django import forms
from django.forms import (
    CheckboxInput, FileInput, NumberInput, Select, SelectMultiple, Textarea,
    TextInput
)

from base.models.inventory import Inventory


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Enter Inventory Name'}),
            'inventory_code': TextInput(attrs={'class': 'form-control', 'id': 'inventory_code',
                                               'placeholder': 'Enter Inventory Code'}),
            'range': Select(attrs={'class': 'form-control', 'id': 'range'}),
            'category': Select(attrs={'class': 'form-control', 'id': 'category'}),
            'color': Select(attrs={'class': 'form-control', 'id': 'color'}),
            'finish': Select(attrs={'class': 'form-control', 'id': 'finish'}),
            'size': Select(attrs={'class': 'form-control', 'id': 'size'}),
            'tags': SelectMultiple(attrs={'class': 'form-control select2', 'id': 'tags', 'multiple': 'multiple'}),
            'short_description': TextInput(
                attrs={'class': 'form-control', 'id': 'short_description',
                       'placeholder': 'Enter inventory shot description'}),
            'full_description': Textarea(attrs={'class': 'form-control', 'id': 'full_description',
                                                'placeholder': 'Enter inventory full description'}),
            'reorder_level': NumberInput(attrs={'class': 'form-control', 'id': 'reorder_level'}),
            'promotional_price': NumberInput(attrs={'class': 'form-control', 'id': 'promotional_price'}),
            'is_promotion': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_promotion'}),
            'wholesale_price': NumberInput(attrs={'class': 'form-control', 'id': 'wholesale_price'}),
            'wholesale_minimum_number': NumberInput(attrs={'class': 'form-control', 'id': 'wholesale_minimum_number'}),
            'picture': FileInput(attrs={'class': 'form-control', 'id': 'picture'}),
            'current_stock': NumberInput(attrs={'class': 'form-control', 'id': 'current_stock'}),
            'selling_price': NumberInput(attrs={'class': 'form-control', 'id': 'selling_price'}),
            'min_selling_price': NumberInput(attrs={'class': 'form-control', 'id': 'min_selling_price'}),
            'stock_unit': TextInput(attrs={'class': 'form-control', 'id': 'stock_unit'})
        }
