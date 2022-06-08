from django.core.exceptions import ValidationError
from django.forms import ModelForm, Select, Textarea, RadioSelect

from base.models.credit_note import CreditNote


class CreditNoteForm(ModelForm):
    class Meta:
        model = CreditNote
        fields = '__all__'

        CHOICES = [
            (True, True),
            (False, False),
        ]

        widgets = {
            'sales_item': Select(attrs={'class': 'form-control', 'id': 'sales_item'}),
            'affects_cash': RadioSelect(attrs={'class': 'form-control', 'id': 'affects_cash'}, choices=CHOICES),
            'credit_note_reason': Textarea(attrs={'class': 'form-control', 'id': 'credit_note_reason'}),
        }
