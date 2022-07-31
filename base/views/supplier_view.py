
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from base.forms.supplier_form import SupplierForm
from base.models.supplier import Supplier


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateSupplierView(SuccessMessageMixin, CreateView):
    template_name = 'supplier/create_supplier.html'
    model = Supplier
    form_class = SupplierForm
    success_url = '/supplier/'

    def get_success_message(self, cleaned_data):
        return f"{self.object.supplier_name} was successfully created!!"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SupplierListView(ListView):
    template_name = 'supplier/supplier_list.html'
    model = Supplier
    context_object_name = 'supplier'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SupplierDetailView(DetailView):
    template_name = 'supplier/supplier_details.html'
    model = Supplier
    context_object_name = 'supplier'


class SupplierUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'supplier/create_supplier.html'
    model = Supplier
    form_class = SupplierForm
    success_url = '/supplier/'

    def get_success_message(self, cleaned_data):
        return f"{self.object.supplier_name} was successfully updated!!"

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SupplierDeleteView(DeleteView):
    template_name = 'supplier/supplier_confirm_delete.html'
    model = Supplier
    success_url = '/supplier/'


def supplier_search(request):
    supplier = Supplier.objects.all()
    query = request.GET.get('q')
    if query:
        supplier = Supplier.objects.filter(
            Q(supplier_name__icontains=query) |
            Q(phone_number_1__icontains=query) |
            Q(phone_number_2__icontains=query) |
            Q(email__icontains=query) |
            Q(physical_address__icontains=query)
        )
    context = {
        'supplier': supplier,
        'query': query
    }

    return render(request, 'supplier/supplier_list.html', context)
