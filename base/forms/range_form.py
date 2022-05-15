from django import forms
from django.forms import TextInput

from base.models.range import Range


class RangeForm(forms.ModelForm):
    class Meta:
        model = Range
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': 'range_name'}),
        }
