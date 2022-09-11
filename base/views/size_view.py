from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.size_form import SizeForm
from base.models.size import Size


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SizeCreateView(SuccessMessageMixin, CreateView):
    template_name = 'size/size_create.html'
    model = Size
    form_class = SizeForm
    success_url = '/size/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Size of type '{form.instance.value} of category {form.instance.category.name}'"
                                       f" successfully created!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SizeListView(ListView):
    template_name = 'size/size_list.html'
    model = Size
    context_object_name = 'size'
    paginate_by = 10


class SizeUpdateView(UpdateView):
    template_name = 'size/size_create.html'
    model = Size
    form_class = SizeForm
    success_url = '/size/'

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        messages.success(self.request, f"Size of type '{form.instance.value} of category {form.instance.category.name}'"
                                       f" successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SizeDeleteView(DeleteView):
    template_name = 'size/size_confirm_delete.html'
    model = Size
    success_url = '/size/'


def size_search(request):
    size = Size.objects.all()
    query = request.GET.get('q')
    if query:
        size = Size.objects.filter(
            Q(category__name__icontains=query) |
            Q(value__icontains=query)
        )
    paginator = Paginator(size, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'size': page_obj,
        'page_obj': page_obj,
        'query': query,
        'is_paginated': True
    }
    return render(request, 'size/size_list.html', context)
