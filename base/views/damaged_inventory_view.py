from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.damaged_inventory_form import DamagedInventoryForm
from base.models import DamagedInventory, Inventory


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DamagedInventoryCreateView(SuccessMessageMixin, CreateView):
    template_name = 'damaged_inventory/damaged_inventory_create.html'
    model = DamagedInventory
    form_class = DamagedInventoryForm
    success_url = '/damaged-inventory/'

    def form_valid(self, form):
        # update Inventory stock
        inventory = Inventory.objects.get(id=form.instance.inventory.id)
        form.instance.quantity_before = inventory.current_stock
        quantity_after = inventory.current_stock - form.instance.count
        form.instance.quantity_after = quantity_after
        inventory.current_stock = quantity_after
        inventory.save()

        form.instance.created_by = self.request.user
        messages.success(self.request, "Damaged Inventory successfully created!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DamagedInventoryListView(ListView):
    template_name = 'damaged_inventory/damaged_inventory_list.html'
    model = DamagedInventory
    context_object_name = 'damaged_inventories'
    paginate_by = 10


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DamagedInventoryUpdateView(UpdateView):
    template_name = 'damaged_inventory/damaged_inventory_create.html'
    model = DamagedInventory
    form_class = DamagedInventoryForm
    success_url = '/damaged-inventory/'

    def form_valid(self, form):

        original_instance = DamagedInventory.objects.get(id=form.instance.id)
        inventory = Inventory.objects.get(id=form.instance.inventory.id)

        if original_instance.inventory.id != form.instance.inventory.id:
            initial_inventory = original_instance.inventory
            initial_inventory.current_stock += original_instance.count
            initial_inventory.save()

        if original_instance.count != form.instance.count:
            inventory.current_stock += original_instance.count

        form.instance.quantity_before = inventory.current_stock
        quantity_after = inventory.current_stock - form.instance.count
        form.instance.quantity_after = quantity_after
        inventory.current_stock = quantity_after
        inventory.save()

        form.instance.modified_by = self.request.user
        messages.success(self.request, "Damaged Inventory successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DamagedInventoryDeleteView(DeleteView):
    template_name = 'damaged_inventory/damaged_inventory_delete.html'
    model = DamagedInventory
    success_url = '/damaged-inventory/'

    def delete(self, *args, **kwargs):
        id = kwargs.get('pk')
        instance = DamagedInventory.objects.get(id=id)
        inventory = instance.inventory
        inventory.current_stock += instance.count
        inventory.save()
        instance.delete()
        messages.success(self.request, "Damaged Inventory successfully deleted !")
        return redirect('damaged_inventory_list')


def damaged_inventory_confirm_replace(request, id):
    instance = DamagedInventory.objects.get(id=id)
    context = dict()
    context['item'] = instance
    template_name = 'damaged_inventory/damaged_inventory_replace.html'
    return render(request, template_name, context)


def damaged_inventory_replace(request, id):
    instance = DamagedInventory.objects.get(id=id)
    inventory = instance.inventory
    inventory.current_stock += instance.count
    inventory.save()
    instance.replaced = True
    instance.modified_by = request.user
    instance.save()
    messages.success(request, "Damaged Inventory successfully replaced!")
    return redirect('damaged_inventory_list')


def damaged_inventory_search(request):
    damaged_inventories = DamagedInventory.objects.all()
    query = request.GET.get('q')
    if query:
        damaged_inventories = DamagedInventory.objects.filter(
            Q(inventory__name__icontains=query) |
            Q(supplier_name__icontains=query) |
            Q(person__name__icontains=query)
        )

    paginator = Paginator(damaged_inventories, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'damaged_inventories': page_obj,
        'page_obj': page_obj,
        'query': query,
        'is_paginated': True
    }

    return render(request, 'damaged_inventory/damaged_inventory_list.html', context)
