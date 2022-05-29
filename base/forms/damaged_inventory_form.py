from django import forms
from django.forms import CheckboxInput, NumberInput, Select, Textarea

from base.models.damaged_inventory import DamagedInventory


class DamagedInventoryForm(forms.ModelForm):
    quantity_before = forms.IntegerField(required=False)
    quantity_after = forms.IntegerField(required=False)

    class Meta:
        model = DamagedInventory
        fields = '__all__'
        widgets = {
            'inventory': Select(attrs={'class': 'form-control select2', 'id': 'inventory'}),
            'supplier': Select(attrs={'class': 'form-control select2', 'id': 'supplier'}),
            'person': Select(attrs={'class': 'form-control select2', 'id': 'person'}),
            'count': NumberInput(attrs={'class': 'form-control', 'id': 'count'}),
            'quantity_before': NumberInput(attrs={'class': 'form-control', 'id': 'quantity_before'}),
            'quantity_after': NumberInput(attrs={'class': 'form-control', 'id': 'quantity_after'}),
            'replaceable':  CheckboxInput(attrs={'class': 'checkbox-inline', 'id': 'replaceable'}),
            'damage_reason': Textarea(attrs={'class': 'form-control', 'id': 'damage_reason'}),
        }
