from django import forms
from django.forms import Select, TextInput

from base.models.size import Size


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = '__all__'
        widgets = {
            'size_type': Select(attrs={
                'class': 'form-control',
                'id': 'size_value',
                'type': 'text'
                }),
            'value': TextInput(attrs={
                'class': 'form-control',
                'id': 'size_value',
                'type': 'number'
                }),
            'category': Select(attrs={
                'class': 'form-control',
                'id': 'size_category'
                })
        }
