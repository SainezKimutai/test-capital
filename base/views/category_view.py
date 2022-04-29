from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.category_form import CategoryForm
from base.models.category import Category


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryCreateView(SuccessMessageMixin, CreateView):
    template_name = 'category/create_category.html'
    success_message = "Category successfully created!"
    model = Category
    form_class = CategoryForm
    success_url = '/create-category/'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryListView(ListView):
    template_name = 'category/category_list.html'
    model = Category
    context_object_name = 'category'
    paginate_by = 10


class CategoryUpdateView(UpdateView):
    template_name = 'category/create_category.html'
    model = Category
    form_class = CategoryForm
    success_url = '/category/'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryDeleteView(DeleteView):
    template_name = 'category/category_confirm_delete.html'
    model = Category
    success_url = '/category/'
