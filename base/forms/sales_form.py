from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, MultipleChoiceField, NumberInput, Select

from base.models.sales import SalesOrder


class SalesOrderForm(ModelForm):

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
        choices=SalesOrder.TRANSACTION_TYPE,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', "multiple": "multiple", 'id': 'transaction_type'})
    )

    class Meta:
        model = SalesOrder
        fields = '__all__'

        widgets = {
            'customer': Select(attrs={'class': 'form-control select2', 'id': 'customer'}),
            'sales_agent': Select(attrs={'class': 'form-control select2', 'id': 'sales_agent'}),
        }

    def __init__(self, *args, **kwargs):
        self.total_amount = None
        super(SalesOrderForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get("customer")
        transaction_type = cleaned_data.get("transaction_type")
        cash_paid = cleaned_data.get("cash_paid")
        mpesa_paid = cleaned_data.get("mpesa_paid")
        if not cash_paid:
            cash_paid = 0
        if not mpesa_paid:
            mpesa_paid = 0

        if SalesOrder.TRANSACTION_TYPE.CREDIT in transaction_type:
            if not customer:
                raise ValidationError("CREDIT transactions must be attached to a customer qualified for credit.")
            else:
                if not customer.is_credit:
                    raise ValidationError("Customer selected is not a credit customer.")

        if SalesOrder.TRANSACTION_TYPE.CREDIT not in transaction_type:
            if (cash_paid + mpesa_paid) < self.total_amount:
                raise ValidationError(f"Amount paid {cash_paid + mpesa_paid} cannot be less than total amount {self.total_amount}.")
