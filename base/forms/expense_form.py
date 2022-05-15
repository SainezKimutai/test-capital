from django import forms
from django.forms import NumberInput, Select, TextInput

from base.models.expense import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'description': TextInput(
                attrs={'class': 'form-control', 'id': 'description', 'placeholder': 'Enter Expense Description'}),
            'amount': NumberInput(
                attrs={'class': 'form-control', 'id': 'amount'}),
            'requester': Select(attrs={'class': 'form-control', 'id': 'requester'}),
        }
