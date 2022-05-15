
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from base.forms.customer_form import CustomerForm
from base.models.customer import Customer


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateCustomerView(SuccessMessageMixin, CreateView):
    template_name = 'customer/create_customer.html'
    model = Customer
    form_class = CustomerForm
    success_url = '/customer/'

    def get_success_message(self, cleaned_data):
        return f"{self.object.name} was successfully created!!"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Customer successfully created!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CustomerListView(ListView):
    template_name = 'customer/customer_list.html'
    model = Customer
    context_object_name = 'customer'
    paginate_by = 10


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CustomerDetailView(DetailView):
    template_name = 'customer/customer_details.html'
    model = Customer
    context_object_name = 'customer'


class CustomerUpdateView(UpdateView):
    template_name = 'customer/create_customer.html'
    model = Customer
    form_class = CustomerForm
    success_url = '/customer/'

    def get_success_message(self, cleaned_data):
        return f"{self.object.name} was successfully updated!!"

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CustomerDeleteView(DeleteView):
    template_name = 'customer/customer_confirm_delete.html'
    model = Customer
    success_url = '/customer/'


def customer_search(request):
    customer = Customer.objects.all()
    query = request.GET.get('q')
    if query:
        customer = Customer.objects.filter(
            Q(name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query) |
            Q(physical_address__icontains=query)
        )
    context = {
        'customer': customer,
        'query': query
    }

    return render(request, 'customer/customer_list.html', context)
