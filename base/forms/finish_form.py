from django import forms
from django.forms import Select, TextInput

from base.models.finish import Finish


class FinishForm(forms.ModelForm):
    class Meta:
        model = Finish
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': 'range_name'}),
            'category': Select(attrs={
                'class': 'form-control select2',
                'id': 'finish_category'
            })
        }
