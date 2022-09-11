from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.category_form import CategoryForm
from base.models.category import Category


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryCreateView(SuccessMessageMixin, CreateView):
    template_name = 'category/category_create.html'
    model = Category
    form_class = CategoryForm
    success_url = '/category/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Category '{form.instance.name}' successfully created!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryListView(ListView):
    template_name = 'category/category_list.html'
    model = Category
    context_object_name = 'category'
    paginate_by = 10


class CategoryUpdateView(UpdateView):
    template_name = 'category/category_create.html'
    model = Category
    form_class = CategoryForm
    success_url = '/category/'

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        messages.success(self.request, f"Category '{form.instance.name}' successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryDeleteView(DeleteView):
    template_name = 'category/category_confirm_delete.html'
    model = Category
    success_url = '/category/'


def category_search(request):
    category = Category.objects.all()
    query = request.GET.get('q')
    if query:
        category = Category.objects.filter(Q(name__icontains=query))

    paginator = Paginator(category, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': page_obj,
        'page_obj': page_obj,
        'query': query,
        'is_paginated': True
    }

    return render(request, 'category/category_list.html', context)
