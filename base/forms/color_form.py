from django import forms
from django.forms import Select, TextInput

from base.models.color import Color


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'

        widgets = {
            'code': TextInput(attrs={
                'class': 'form-control',
                'id': 'color_name',
                'type': 'color'
            }),
            'name': TextInput(attrs={
                'class': 'form-control',
                'id': 'color_name',
                'type': 'text'
            }),
            'category': Select(attrs={
                'class': 'form-control select2',
                'id': 'color_category'
            })
        }
