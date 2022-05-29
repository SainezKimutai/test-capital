from django import forms
from django.forms import DateInput, NumberInput, Select, Textarea

from base.models.promotion import Promotion


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'
        widgets = {
            'inventory': Select(attrs={'class': 'form-control', 'id': 'inventory'}),
            'promotion_price': NumberInput(attrs={'class': 'form-control', 'id': 'promotion_price'}),
            'promotion_start_date': DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'id': 'promotion_price', 'type': 'date'}),
            'promotion_end_date': DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'id': 'promotion_price', 'type': 'date'}),
            'description': Textarea(attrs={'class': 'form-control', 'id': 'description'}),
        }
