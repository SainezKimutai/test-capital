from django import forms
from django.forms import Textarea, TextInput

from base.models.supplier import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'supplier_name': TextInput(attrs={'class': 'form-control', 'id': 'supplier_name', 'placeholder': 'Enter Supplier Name'}),
            'phone_number_1': TextInput(attrs={'class': 'form-control', 'id': 'phone_number_1', 'placeholder': 'Enter phone number +254'}),
            'phone_number_2': TextInput(attrs={'class': 'form-control', 'id': 'phone_number_2'}),
            'contact_person': TextInput(attrs={'class': 'form-control', 'id': 'contact_person'}),
            'vat_number': TextInput(attrs={'class': 'form-control', 'id': 'vat_number'}),
            'pin_number': TextInput(attrs={'class': 'form-control', 'id': 'pin_number'}),
            'email': TextInput(attrs={'class': 'form-control', 'id': 'email'}),
            'physical_address': Textarea(attrs={'class': 'form-control', 'id': 'physical_address',
                                                'placeholder': 'Enter physical address description'}),
        }
