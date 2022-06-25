from django import forms
from django.forms import DateInput, NumberInput, Select, Textarea

from base.models.promotion import Promotion


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'
        widgets = {
            'inventory': Select(attrs={'class': 'form-control', 'id': 'inventory'}),
            'promotion_price': NumberInput(attrs={'class': 'form-control', 'id': 'promotion_price', 'min': '1'}),
            'promotion_start_date': DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'id': 'promotion_price', 'type': 'date'}),
            'promotion_end_date': DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'id': 'promotion_price', 'type': 'date'}),
            'description': Textarea(attrs={'class': 'form-control', 'id': 'description'}),
        }

    def clean(self):
        form_data = self.cleaned_data
        if form_data['promotion_start_date'] > form_data['promotion_end_date']:
            self._errors["promotion_end_date"] = ["End date should be a day after start date"]
            del form_data['promotion_end_date']
        overlap, overlap_range = self.overlap(form_data['promotion_start_date'], form_data['promotion_end_date'])
        if overlap:
            self._errors["promotion_range"] = [f"Dates entered overlaps with existing range {overlap_range}"]
            self._errors["promotion_start_date"] = ["Adjust date range"]
            self._errors["promotion_end_date"] = ["Adjust date range"]
            del form_data['promotion_start_date']
            del form_data['promotion_end_date']
        return form_data

    def overlap(self, start, end):
        all_promotions = Promotion.objects.filter(inventory=self.cleaned_data['inventory'])
        overlap = False
        overlap_range = None
        for promotion_item in all_promotions:
            if promotion_item.promotion_start_date < start < promotion_item.promotion_end_date:
                overlap = True
                overlap_range = f'{promotion_item.promotion_start_date} to {promotion_item.promotion_end_date}'
                break
            elif promotion_item.promotion_start_date < end < promotion_item.promotion_end_date:
                overlap = True
                overlap_range = f'{promotion_item.promotion_start_date} to {promotion_item.promotion_end_date}'
                break
        return overlap, overlap_range
