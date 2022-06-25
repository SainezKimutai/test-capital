from django import forms
from django.contrib.auth.models import User
from django.forms import CheckboxInput, NumberInput, Select, Textarea

from base.models.damaged_inventory import DamagedInventory
from base.models.supplier import Supplier


class DamagedInventoryForm(forms.ModelForm):
    quantity_before = forms.IntegerField(required=False)
    quantity_after = forms.IntegerField(required=False)
    replaced = forms.BooleanField(required=False)
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        required=False,
        widget=Select(attrs={'class': 'form-control', 'id': 'supplier'})
    )
    person = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=Select(attrs={'class': 'form-control', 'id': 'person'})
    )

    class Meta:
        model = DamagedInventory
        fields = '__all__'
        widgets = {
            'inventory': Select(attrs={'class': 'form-control', 'id': 'inventory'}),
            'count': NumberInput(attrs={'class': 'form-control', 'id': 'count', 'min': '1'}),
            'replaceable':  CheckboxInput(attrs={'class': 'checkbox-inline', 'id': 'replaceable'}),
            'damage_reason': Textarea(attrs={'class': 'form-control', 'id': 'damage_reason'}),
        }

    def clean(self):
        form_data = self.cleaned_data
        if form_data['count'] > form_data['inventory'].current_stock:
            self._errors["count"] = [f"Count cannot exceed inventory current stock, {form_data['inventory'].current_stock}"]
            del form_data['count']

        if form_data['replaceable'] and not form_data['supplier']:
            self._errors["supplier"] = ["You have to select a supplier if items are replaceable"]
            del form_data['supplier']
        return form_data
