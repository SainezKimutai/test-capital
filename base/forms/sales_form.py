from django.core.exceptions import ValidationError
from django.forms import ModelForm, Select

from base.models.sales import SalesOrder


class SalesOrderForm(ModelForm):
    class Meta:
        model = SalesOrder
        fields = '__all__'

        widgets = {
            'customer': Select(attrs={'class': 'form-control', 'id': 'customer'}),
            'sales_agent': Select(attrs={'class': 'form-control', 'id': 'sales_agent'}),
            'transaction_type': Select(attrs={'class': 'form-control', 'id': 'transaction_type'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get("customer")
        transaction_type = cleaned_data.get("transaction_type")

        if transaction_type == SalesOrder.TRANSACTION_TYPE.CREDIT:
            if not customer:
                raise ValidationError("CREDIT transactions must be attached to a customer qualified for credit.")
            else:
                if not customer.is_credit:
                    raise ValidationError("Customer selected is not a credit customer.")
