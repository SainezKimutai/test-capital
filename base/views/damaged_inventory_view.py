from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
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


class DamagedInventoryUpdateView(UpdateView):
    template_name = 'damaged_inventory/damaged_inventory_create.html'
    model = DamagedInventory
    form_class = DamagedInventoryForm
    success_url = '/damaged-inventory/'

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        messages.success(self.request, "DamagedInventory successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DamagedInventoryDeleteView(DeleteView):
    template_name = 'damaged_inventory/damaged_inventory_delete.html'
    model = DamagedInventory
    success_url = '/damaged-inventory/'


def damaged_inventory_search(request):
    damaged_inventories = DamagedInventory.objects.all()
    query = request.GET.get('q')
    if query:
        damaged_inventories = DamagedInventory.objects.filter(
            Q(inventory__name__icontains=query) |
            Q(supplier_name__icontains=query) |
            Q(person__name__icontains=query)
        )
    context = {
        'damaged_inventories': damaged_inventories,
        'query': query
    }
    return render(request, 'damaged_inventory/damaged_inventory_list.html', context)
