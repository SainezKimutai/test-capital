import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from base.forms.inventory_form import InventoryForm
from base.helper import bulk_edit_headers, clean_file_to_array
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
            Q(size__value=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        )
    paginator = Paginator(inventory, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'inventory': page_obj,
        'page_obj': page_obj,
        'query': query,
        'is_paginated': True
    }

    return render(request, 'inventory/inventory_list.html', context)


def inventory_bulk_edit_page(request):
    context = dict()
    context['inventory_csv']: None
    context['errors'] = []
    return render(request, 'inventory/inventory_bulk_edit.html', context)


def inventory_download(request):
    inventory = Inventory.objects.values(
        'id',
        'name',
        'color__name',
        'range__name',
        'category__name',
        'finish__name',
        'size__value',
        'current_stock',
        'recent_buying_price',
        'max_selling_price',
        'min_selling_price',
        'selling_price',
        'wholesale_price',
        'wholesale_minimum_number'
    )
    headers = bulk_edit_headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="list_of_all_inventories.csv"'

    writer = csv.DictWriter(response, fieldnames=headers)
    writer.writeheader()
    writer.writerows(inventory)

    return response


def inventory_bulk_edit_update(request):
    request_file = request.FILES

    if 'inventory_csv' in request_file:
        uploaded_file = request_file['inventory_csv']
        if not uploaded_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return redirect(reverse('inventory_bulk_edit_page'))

        decoded_file = uploaded_file.read().decode('utf-8')
        file_contents = clean_file_to_array(decoded_file)

        headers = file_contents[0]

        if headers != bulk_edit_headers:
            messages.error(request, 'Unexpected file headers')

            return redirect(reverse('inventory_bulk_edit_page'))

        inventories = Inventory.objects.all()
        file_rows = file_contents[1:]

        validation_errors = []
        for row in file_rows:
            inventory = inventories.get(id=row[0])

            inventory.current_stock = row[7]
            inventory.recent_buying_price = row[8]
            inventory.max_selling_price = row[9]
            inventory.min_selling_price = row[10]
            inventory.selling_price = row[11]
            inventory.wholesale_price = row[12]
            inventory.wholesale_minimum_number = row[13]

            inventory.modified_by = request.user

            try:
                inventory.save()
            except Exception as inst:
                for error in inst.args:
                    if error:
                        error_msg = f"{inventory.name}, {list(error.values())[0]}"
                        validation_errors.append(error_msg)

        if len(validation_errors):
            context = dict()
            context['inventory_csv']: None
            context['errors'] = validation_errors
            messages.error(request, 'Upload validation failed')

            return render(request, 'inventory/inventory_bulk_edit.html', context)

        messages.success(request, 'Invetories successfully updated')
        return redirect(reverse('inventory_list'))

    else:
        messages.warning(request, 'Kindly upload a file..')
        return redirect(reverse('inventory_bulk_edit_page'))
