from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.range_form import RangeForm
from base.models.range import Range


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RangeCreateView(SuccessMessageMixin, CreateView):
    template_name = 'range/range_create.html'
    model = Range
    form_class = RangeForm
    success_url = '/range/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Range '{form.instance.name}' successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RangeListView(ListView):
    template_name = 'range/range_list.html'
    model = Range
    context_object_name = 'range'
    paginate_by = 10


class RangeUpdateView(UpdateView):
    template_name = 'range/range_create.html'
    model = Range
    form_class = RangeForm
    success_url = '/range/'

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        messages.success(self.request, f"Range '{form.instance.name}' successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RangeDeleteView(DeleteView):
    template_name = 'range/range_confirm_delete.html'
    model = Range
    success_url = '/range/'


def range_search(request):
    range = Range.objects.all()
    query = request.GET.get('q')
    if query:
        range = Range.objects.filter(
            Q(name__icontains=query)
        )
    paginator = Paginator(range, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'range': page_obj,
        'page_obj': page_obj,
        'query': query,
        'is_paginated': True
    }

    return render(request, 'range/range_list.html', context)
