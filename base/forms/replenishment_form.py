from django import forms
from django.forms import NumberInput, Select
from django.forms.models import inlineformset_factory

from base.models.replenishment import Replenishment, ReplenishmentItem


class ReplenishmentForm(forms.ModelForm):
    total_amount = forms.DecimalField(required=False)
    receipt_number = forms.CharField(required=False)

    class Meta:
        model = Replenishment
        fields = '__all__'

        widgets = {
            'supplier': Select(attrs={
                'class': 'form-control',
                'id': 'replenishment_supplier'
            })
        }


class ReplenishmentItemForm(forms.ModelForm):
    class Meta:
        model = ReplenishmentItem
        fields = '__all__'

        widgets = {
            'inventory': Select(attrs={
                'class': 'form-control',
                'id': 'replenishment_inventory'
            }),
            'replenishment': Select(attrs={
                'class': 'form-control',
                'id': 'replenishment_inventory'
            }),
            'count': NumberInput(attrs={'class': 'form-control', 'id': 'replenishment_count'}),
            'amount': NumberInput(attrs={'class': 'form-control', 'id': 'replenishment_amount'})
        }


ReplenishmentItemInlineFormset = inlineformset_factory(
    Replenishment,
    ReplenishmentItem,
    form=ReplenishmentItemForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True
)
