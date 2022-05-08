from django import forms
from django.forms import TextInput, Select

from base.models.color import Color


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color 
        fields = '__all__'

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'category': Select(attrs={'class': 'form-control'})
        }