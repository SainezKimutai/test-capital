from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from base.forms.invoice_form import InvoiceOrderForm
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
    form = InvoiceOrderForm(request.POST or None)
    if not invoice.paid and invoice.pending_balance == 0:
        invoice.pending_balance = invoice.sales_order.total_amount
    if request.method == 'POST':
        if form.is_valid():
            form_data = form.cleaned_data
            cash_paid = form_data.get('cash_paid') if form_data.get('cash_paid') else 0
            mpesa_paid = form_data.get('mpesa_paid') if form_data.get('mpesa_paid') else 0
            total_cash_paid = invoice.cash_paid + cash_paid
            total_mpesa_paid = invoice.mpesa_paid + mpesa_paid
            total_amount_paid = total_mpesa_paid + total_cash_paid
            total_amount_balance = invoice.sales_order.total_amount - total_amount_paid
            invoice.pending_balance = total_amount_balance

            if total_amount_balance <= 0:
                invoice.paid = True
                invoice.payment_status = Invoice.PAYMENT_STATUS.FULLY_PAID
            else:
                invoice.payment_status = Invoice.PAYMENT_STATUS.PARTIALLY_PAID

            transaction = []
            if total_mpesa_paid > 0:
                transaction.append(Invoice.TRANSACTION_TYPE.MPESA)
            if total_cash_paid > 0:
                transaction.append(Invoice.TRANSACTION_TYPE.CASH)
            invoice.cash_paid = total_cash_paid
            invoice.mpesa_paid = total_mpesa_paid
            invoice.transaction_type = transaction
            invoice.payment_date = date.today()
            invoice.modified_by = request.user
            invoice.save()
            messages.add_message(request, messages.INFO, 'Invoice successfully updated.')
            return redirect('invoice_list')

    return render(request, 'invoice/invoice_mark_as_paid.html', {'invoice': invoice, 'form': form})


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
