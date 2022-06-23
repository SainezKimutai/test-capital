from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from base.forms.inventory_form import InventoryForm
from base.models.inventory import Inventory


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateInventoryView(SuccessMessageMixin, CreateView):
    template_name = 'inventory/create_inventory.html'
    model = Inventory
    form_class = InventoryForm
    success_url = '/inventory/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Inventory '{form.instance.name}' successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InventoryListView(ListView):
    template_name = 'inventory/inventory_list.html'
    model = Inventory
    context_object_name = 'inventory'
    paginate_by = 10


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InventoryDetailView(DetailView):
    template_name = 'inventory/inventory_details.html'
    model = Inventory
    context_object_name = 'inventory'


class InventoryUpdateView(UpdateView):
    template_name = 'inventory/create_inventory.html'
    model = Inventory
    form_class = InventoryForm
    success_url = '/inventory/'

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        messages.success(self.request, f"Inventory '{form.instance.name}' successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InventoryDeleteView(DeleteView):
    template_name = 'inventory/inventory_confirm_delete.html'
    model = Inventory
    success_url = '/inventory/'


def inventory_search(request):
    inventory = Inventory.objects.all()
    query = request.GET.get('q')
    if query:
        inventory = Inventory.objects.filter(
            Q(short_description__icontains=query) |
            Q(full_description__icontains=query) |
            Q(name__icontains=query) |
            Q(range__name__icontains=query) |
            Q(color__name__icontains=query) |
            Q(finish__name__icontains=query) |
            Q(size__size_type=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        )
    context = {
        'inventory': inventory,
        'query': query
    }
    return render(request, 'inventory/inventory_list.html', context)
