from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from base.models.invoice import Invoice


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InvoiceListView(ListView):
    template_name = 'invoice/invoice_list.html'
    model = Invoice
    context_object_name = 'invoice'
    paginate_by = 10


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class InvoiceDetailView(DetailView):
    template_name = 'invoice/invoice_details.html'
    model = Invoice
    context_object_name = 'invoice'


@login_required
def mark_invoice_as_paid(request, pk):
    invoice = Invoice.objects.get(id=pk)

    if request.method == 'POST':
        invoice.paid = True
        invoice.payment_date = date.today()
        invoice.modified_by = request.user
        invoice.save()
        messages.add_message(request, messages.INFO, 'Invoice successfully marked as PAID.')
        return redirect('invoice_list')

    return render(request, 'invoice/invoice_mark_as_paid.html', {'invoice': invoice})


def invoice_search(request):
    invoice = Invoice.objects.all()
    query = request.GET.get('q')
    if query:
        invoice = Invoice.objects.filter(
            Q(sales_order__customer__name__icontains=query) |
            Q(sales_order__customer__phone_number__icontains=query) |
            Q(sales_order__receipt_number__icontains=query) |
            Q(paid__icontains=query)
        )

    paginator = Paginator(invoice, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'invoice': page_obj,
        'page_obj': page_obj,
        'query': query,
        'is_paginated': True
    }

    return render(request, 'invoice/invoice_list.html', context)
