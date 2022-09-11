import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import ListView

from base.addcart import Cart
from base.forms.sales_form import SalesOrderForm
from base.models.invoice import Invoice
from base.models.sales import SalesItem, SalesOrder


def make_payment_view(request):
    cart = Cart(request)
    form = SalesOrderForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            order = form.save()
            order.created_by = request.user
            order.total_amount = cart.get_total_price()
            order.modified_by = request.user
            order.save()
            for item in cart:
                inventory = item['inventory']
                SalesItem.objects.create(
                    sales_order=order,
                    inventory=inventory,
                    price=item['price'],
                    quantity=item['quantity'],
                    total_amount=item['quantity'] * item['price']
                )
                # Update inventory to reduce the count
                inventory.current_stock = inventory.current_stock - item['quantity']
                inventory.save()

            cart.clear()

            # Create invoice if transaction was credit
            if order.transaction_type == SalesOrder.TRANSACTION_TYPE.CREDIT:
                expected_payment_date = datetime.date.today() + datetime.timedelta(
                    order.customer.days_to_clear_invoice)
                Invoice.objects.create(
                    sales_order=order,
                    expected_payment_date=expected_payment_date,
                    created_by=request.user
                )
            return redirect('pos_view')
    return render(request, 'pos/sales_order_information.html', {'form': form, 'cart': cart})


class SalesItemView(ListView):
    template_name = 'pos/sales_item_list.html'
    model = SalesItem
    context_object_name = 'sales_item'
    paginate_by = 10


def sales_order_search(request):
    sales_item = SalesItem.objects.all()
    query = request.GET.get('q')
    if query:
        sales_item = SalesItem.objects.filter(
            Q(sales_order__customer__name__icontains=query) |
            Q(sales_order__sales_agent__username__icontains=query) |
            Q(sales_order__sales_agent__first_name__icontains=query) |
            Q(sales_order__sales_agent__last_name__icontains=query) |
            Q(sales_order__receipt_number__icontains=query) |
            Q(inventory__name__icontains=query) |
            Q(sales_order__transaction_type__icontains=query)
        )
    paginator = Paginator(sales_item, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sales_item': page_obj,
        'page_obj': page_obj,
        'query': query,
        'is_paginated': True
    }

    return render(request, 'pos/sales_item_list.html', context)
