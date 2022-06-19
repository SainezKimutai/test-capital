from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.forms import (
    CheckboxInput, ModelForm, NumberInput, Select, Textarea
)
from django.utils.datastructures import MultiValueDict

from base.models.credit_note import CreditNote


class CreditNoteForm(ModelForm):
    class Meta:
        model = CreditNote
        fields = '__all__'

        widgets = {
            'sales_item': Select(attrs={'class': 'form-control', 'id': 'sales_item', 'readonly': True,
                                        'required': False, 'disabled': True}),
            'quantity': NumberInput(attrs={'class': 'form-control', 'id': 'quantity', 'required': True}),
            'affects_cash': CheckboxInput(attrs={'class': 'form-control', 'id': 'affects_cash', 'required': True},
                                          ),
            'credit_note_reason': Textarea(attrs={'class': 'form-control', 'id': 'credit_note_reason', 'required': True
                                                  }),
        }

    def __init__(self, data, **kwargs):
        if data:
            initial = kwargs.get("initial", {})
            data = MultiValueDict({**{k: [v] for k, v in initial.items()}, **data})
        super().__init__(data, **kwargs)

    def clean_quantity(self):
        sale_item = self.cleaned_data['sales_item']
        data = self.cleaned_data['quantity']

        # Check if there exists previous credit_notes for this sale item
        # If so, esnure the quantity doesn't exceed sale item quantity
        previous_quantity = CreditNote.objects.filter(sales_item=sale_item)

        if previous_quantity:
            count = previous_quantity.aggregate(Sum('quantity')).get('quantity__sum') + data
        else:
            count = data

        if count > sale_item.quantity:
            raise ValidationError(f"Quantity exceeds sale item quantity. {count} quantity already raised. Max quantity"
                                  f" is {sale_item.quantity}")

        if data == 0:
            raise ValidationError(f"Quantity cannot be 0.")

        return data
