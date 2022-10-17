from django import forms
from django.forms import ModelForm, MultipleChoiceField, NumberInput

from base.models.invoice import Invoice


class InvoiceOrderForm(ModelForm):

    sales_order = forms.IntegerField(required=False)

    expected_payment_date = forms.DateField(required=False)

    cash_paid = forms.IntegerField(
        required=False,
        widget=NumberInput(attrs={'class': 'form-control', 'id': 'cash_paid', 'min': '1'})
    )

    mpesa_paid = forms.IntegerField(
        required=False,
        widget=NumberInput(attrs={'class': 'form-control', 'id': 'mpesa_paid', 'min': '1'})
    )
    transaction_type = MultipleChoiceField(
        required=True,
        choices=Invoice.TRANSACTION_TYPE,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', "multiple": "multiple", 'id': 'transaction_type'})
    )

    class Meta:
        model = Invoice
        fields = '__all__'
