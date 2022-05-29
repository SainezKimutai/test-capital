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
