from django.forms import EmailInput, ModelForm, NumberInput, TextInput

from base.models.order import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

        widgets = {
            'full_name': TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Enter Full Name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Enter email address'}),
            'phn_number': NumberInput(attrs={'class': 'form-control', 'id': 'phn_number'}),
            'address': TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Enter address'})
        }
