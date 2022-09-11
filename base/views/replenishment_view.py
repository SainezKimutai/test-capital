import copy
import random
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, ListView

from base.helper import generate_receipt
from base.models import Inventory, Replenishment, ReplenishmentItem, Supplier
from base.replenishment_helper import ReplenishmentEntry


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ReplenishmentView(View):
    def get(self, request):
        context = dict()
        replenishment_object = ReplenishmentEntry(request)
        replenishment_entry = replenishment_object.replenishment_entry

        context['replenishment'] = replenishment_entry
        context['inventories'] = Inventory.objects.all()
        context['suppliers'] = Supplier.objects.all()
        context['error'] = []
        template_name = 'replenishment/replenishment_create.html'
        return render(request, template_name, context)


@require_POST
def replenishment_add(request):
    template_name = 'replenishment/replenishment_create.html'
    replenishment_object = ReplenishmentEntry(request)
    context = dict()
    context['replenishment'] = replenishment_object.replenishment_entry
    context['inventories'] = Inventory.objects.all()
    context['suppliers'] = Supplier.objects.all()
    context['errors'] = []

    inventory_id = request.POST.get('inventory_id', None)
    if not inventory_id:
        context['errors'].append('Add item inventory')

    count = request.POST.get('count', None)
    if not count:
        context['errors'].append('Add item count')

    amount = request.POST.get('amount', None)
    if not amount:
        context['errors'].append('Add item amount')

    if context['errors']:
        return render(request, template_name, context)
    item = {
        'id': random.randint(0, 100000),
        'inventory_id': int(inventory_id),
        'count': int(count),
        'amount': amount,
    }

    replenishment_object.add(item=item)

    context['replenishment'] = copy.deepcopy(replenishment_object.replenishment_entry)

    context['replenishment']['items'] = context['replenishment']['items'] + context['replenishment']['added_items']

    template_name = 'replenishment/replenishment_create.html'
    return render(request, template_name, context)


def replenishment_update(request, id):
    replenishment_instance = get_object_or_404(Replenishment, id=id)
    replenishment_items = ReplenishmentItem.objects.filter(replenishment=replenishment_instance)

    replenishment_object = ReplenishmentEntry(request)

    replenishment_object.update(replenishment={
        'supplier_id': replenishment_instance.supplier.id,
        'delivery_number': replenishment_instance.delivery_number,
        'id': replenishment_instance.id
    })

    for item in replenishment_items:
        item_obj = {
            'id': item.id,
            'inventory_id': item.inventory.id,
            'count': int(item.count),
            'amount': int(item.amount),
        }
        replenishment_object.add(item=item_obj)
    replenishment_object.update(new_entry=False)
    context = dict()
    context['replenishment'] = replenishment_object.replenishment_entry
    context['inventories'] = Inventory.objects.all()
    context['suppliers'] = Supplier.objects.all()
    context['error'] = []
    template_name = 'replenishment/replenishment_create.html'
    return render(request, template_name, context)


@require_POST
def replenishment_item_update(request, id):
    template_name = 'replenishment/replenishment_create.html'
    replenishment_object = ReplenishmentEntry(request)
    context = dict()
    context['replenishment'] = replenishment_object.replenishment_entry
    context['inventories'] = Inventory.objects.all()
    context['suppliers'] = Supplier.objects.all()
    context['errors'] = []

    inventory_id = request.POST.get('inventory_id', None)
    if not inventory_id:
        context['errors'].append('Add item inventory')

    count = request.POST.get('count', None)
    if not count:
        context['errors'].append('Add item count')

    amount = request.POST.get('amount', None)
    if not amount:
        context['errors'].append('Add item amount')

    if context['errors']:
        return render(request, template_name, context)
    item = {
        'id': id,
        'inventory_id': inventory_id,
        'count': count,
        'amount': amount,
    }
    replenishment_object.update(item=item)
    context['replenishment'] = replenishment_object.replenishment_entry

    return render(request, template_name, context)


def replenishment_remove(request, id):
    replenishment_object = ReplenishmentEntry(request)

    replenishment_object.remove(item_id=id)
    context = dict()
    context['replenishment'] = replenishment_object.replenishment_entry
    context['inventories'] = Inventory.objects.all()
    context['suppliers'] = Supplier.objects.all()
    context['error'] = []
    template_name = 'replenishment/replenishment_create.html'
    return render(request, template_name, context)


def replenishment_save(request):
    replenishment_object = ReplenishmentEntry(request)

    context = dict()
    context['errors'] = []
    template_name = 'replenishment/replenishment_create.html'

    supplier_id = request.POST.get('supplier_id', None)

    if not supplier_id:
        context['errors'].append('No Supplier selected')
    else:
        replenishment_object.update(replenishment={'supplier_id': supplier_id})

    delivery_number = request.POST.get('delivery_number', None)
    if not delivery_number:
        context['errors'].append('No Delivery Number')
    else:
        replenishment_object.update(replenishment={'delivery_number': delivery_number})

    context['replenishment'] = replenishment_object.replenishment_entry
    context['inventories'] = Inventory.objects.all()
    context['suppliers'] = Supplier.objects.all()

    items = replenishment_object.replenishment_entry['items']
    if not items:
        context['errors'].append('Add atleast one item')

    if context['errors']:
        return render(request, template_name, context)

    if replenishment_object.replenishment_entry['new_entry']:
        created_replenishment = Replenishment.objects.create(
            receipt_number=generate_receipt(Replenishment, 'RPL'),
            supplier=get_object_or_404(Supplier, id=supplier_id),
            delivery_number=delivery_number,
            total_amount=0,
            created_by=request.user
        )

        for item in items:
            inventory = get_object_or_404(Inventory, id=item['inventory_id'])
            ReplenishmentItem.objects.create(
                replenishment=created_replenishment,
                inventory=inventory,
                count=int(item['count']),
                amount=Decimal(item['amount'])
            )
            total_item_amount = int(item['count']) * Decimal(item['amount'])
            created_replenishment.total_amount += total_item_amount

            # Update Inventory
            inventory.current_stock += int(item['count'])
            inventory.recent_buying_price = Decimal(item['amount'])
            inventory.save()

        created_replenishment.save()
    else:
        id = replenishment_object.replenishment_entry['id']
        updated_replenishment = get_object_or_404(Replenishment, id=id)
        updated_replenishment.supplier = get_object_or_404(Supplier, id=supplier_id)
        updated_replenishment.delivery_number = delivery_number
        updated_replenishment.modified_by = request.user
        updated_replenishment.save()

        # Inventory Count or amount change
        for item in items:
            item_instance = get_object_or_404(ReplenishmentItem, id=item['id'])

            if item['inventory_id'] != item_instance.inventory.id:
                inventory = item_instance.inventory
                inventory.current_stock -= item_instance.count

                replenishment_items = ReplenishmentItem.objects.filter(inventory=inventory).order_by('-id')
                lastest_item = replenishment_items[0].id == item_instance.id
                if lastest_item:
                    second_last_item = replenishment_items[1] if len(replenishment_items) > 1 else None
                    inventory.recent_buying_price = second_last_item.amount if second_last_item else 0

                inventory.save()

                new_inventory = get_object_or_404(Inventory, id=item['inventory_id'])
                new_inventory.current_stock += int(item['count'])
                new_inventory.recent_buying_price = Decimal(item['amount'])
                new_inventory.save()
                item_instance.inventory = new_inventory

                item_instance.count = int(item['count'])
                item_instance.amount = Decimal(item['amount'])

            else:
                if int(item['count']) != item_instance.count:
                    inventory = item_instance.inventory
                    inventory.current_stock -= item_instance.count
                    inventory.current_stock += int(item['count'])
                    inventory.save()

                    item_instance.count = int(item['count'])

                if Decimal(item['amount']) != item_instance.amount:
                    inventory = item_instance.inventory
                    inventory.recent_buying_price = Decimal(item['amount'])
                    inventory.save()

                    item_instance.amount = Decimal(item['amount'])

            inventory = item_instance.inventory
            inventory.modified_by = request.user

            item_instance.save()

        # Added Items
        added_items = replenishment_object.replenishment_entry['added_items']

        for item in added_items:
            inventory = get_object_or_404(Inventory, id=item['inventory_id'])
            ReplenishmentItem.objects.create(
                replenishment=updated_replenishment,
                inventory=inventory,
                count=int(item['count']),
                amount=Decimal(item['amount'])
            )
            # Update Inventory
            inventory.current_stock += int(item['count'])
            inventory.recent_buying_price = Decimal(item['amount'])
            inventory.save()

        # Removed Items
        removed_items = replenishment_object.replenishment_entry['removed_items']
        for item in removed_items:
            item_instance = get_object_or_404(ReplenishmentItem, id=item['id'])
            inventory = item_instance.inventory
            inventory.current_stock -= int(item['count'])

            replenishment_items = ReplenishmentItem.objects.filter(inventory=inventory).order_by('-id')
            lastest_item = replenishment_items[0].id == item_instance.id
            if lastest_item:
                second_last_item = replenishment_items[1] if len(replenishment_items) > 1 else None
                inventory.recent_buying_price = second_last_item.amount if second_last_item else 0

            inventory.save()
            item_instance.delete()

        all_items = ReplenishmentItem.objects.filter(replenishment=updated_replenishment)
        updated_replenishment.total_amount = 0
        for item in all_items:
            total_item_amount = item.count * item.amount
            updated_replenishment.total_amount += total_item_amount

        updated_replenishment.save()

    replenishment_object.clear()
    messages.success(request, "Replenishment was successfully saved!")
    return redirect('replenishment_list')


def replenishment_clear(request):
    replenishment_object = ReplenishmentEntry(request)
    replenishment_object.clear()
    return redirect('replenishment_list')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ReplenishmentListView(ListView):
    template_name = 'replenishment/replenishment_list.html'
    model = Replenishment
    context_object_name = 'replenishments'
    paginate_by = 10


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ReplenishmentDeleteView(DeleteView):
    template_name = 'replenishment/replenishment_confirm_delete.html'
    model = Replenishment
    success_url = '/replenishment/'

    def delete(self, *args, **kwargs):
        id = kwargs.get('pk')
        replenishment = get_object_or_404(Replenishment, id=id)
        replenishment_items = ReplenishmentItem.objects.filter(replenishment=replenishment)
        for item_instance in replenishment_items:
            inventory = item_instance.inventory
            inventory.current_stock -= item_instance.count

            replenishment_items = ReplenishmentItem.objects.filter(inventory=inventory).order_by('-id')
            lastest_item = replenishment_items[0].id == item_instance.id
            if lastest_item:
                second_last_item = replenishment_items[1] if len(replenishment_items) > 1 else None
                inventory.recent_buying_price = second_last_item.amount if second_last_item else 0

            inventory.save()
            item_instance.delete()
        replenishment.delete()
        messages.success(self.request, "Replenishment was successfully deleted!")
        return redirect('replenishment_list')


def replenishment_search(request):
    replenishments = Replenishment.objects.all()
    query = request.GET.get('q')
    if query:
        replenishments = Replenishment.objects.filter(
            Q(receipt_number__icontains=query) |
            Q(supplier__supplier_name__icontains=query)
        )
    paginator = Paginator(replenishments, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'replenishments': page_obj,
        'page_obj': page_obj,
        'query': query,
        'is_paginated': True
    }
    return render(request, 'replenishment/replenishment_list.html', context)
