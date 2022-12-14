from django import forms
from django.forms import CheckboxInput, FileInput, Select, TextInput

from base.models.category import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'parent': Select(attrs={'class': 'form-control select2'}),
            'category_image': FileInput(attrs={'class': 'form-control', 'id': 'imageUpload', 'type': 'file'}),
            'is_active': CheckboxInput(attrs={'class': 'checkbox', 'id': 'is_active'})
        }
