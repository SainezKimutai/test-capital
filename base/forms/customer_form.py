from django import forms
from django.forms import Select, Textarea, TextInput, EmailInput

from base.models.customer import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        is_credit_choices = (
            (True, 'Yes'),
            (False, 'No'),
        )

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Enter Customer Name'}),
            'phone_number': TextInput(attrs={'class': 'form-control', 'id': 'phone_number', 'placeholder': 'Enter phone number +254'}),
            'is_credit': Select(attrs={'class': 'form-control', 'id': 'is_credit'}, choices=is_credit_choices),
            'vat_number': TextInput(attrs={'class': 'form-control', 'id': 'vat_number'}),
            'pin_number': TextInput(attrs={'class': 'form-control', 'id': 'pin_number'}),
            'email': EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
            'physical_address': Textarea(attrs={'class': 'form-control', 'id': 'physical_address',
                                                'placeholder': 'Enter physical address description'}),
        }
