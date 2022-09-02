from django import forms
from django.forms import Select, TextInput

from base.models.size import Size


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = '__all__'
        widgets = {
            'value': TextInput(attrs={
                'class': 'form-control',
                'id': 'size_value',
                'type': 'text'
                }),
            'category': Select(attrs={
                'class': 'form-control select2',
                'id': 'size_category'
                })
        }
