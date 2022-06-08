import datetime

from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import ListView

from base.forms.sales_form import SalesOrderForm
from base.forms.credit_note_form import CreditNoteForm
from base.models.credit_note import CreditNote
from base.models.sales import SalesItem, SalesOrder


def create_credit_note_view(request):
    form = CreditNoteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            pass

            return redirect('pos_view')
    return render(request, 'pos/sales_order_information.html', {'form': form})


class SalesItemView(ListView):
    template_name = 'pos/sales_item_list.html'
    model = SalesItem
    context_object_name = 'sales_item'
    paginate_by = 10


def credit_note_search(request):
    credit_note = CreditNote.objects.all()
    query = request.GET.get('q')
    if query:
        credit_note = CreditNote.objects.filter(
            Q(sales_order__customer__name__icontains=query) |
            Q(sales_order__sales_agent__username__icontains=query) |
            Q(sales_order__sales_agent__first_name__icontains=query) |
            Q(sales_order__sales_agent__last_name__icontains=query) |
            Q(sales_order__receipt_number__icontains=query) |
            Q(inventory__name__icontains=query) |
            Q(sales_order__transaction_type__icontains=query)
        )
    context = {
        'credit_note': credit_note,
        'query': query
    }
    return render(request, 'pos/sales_item_list.html', context)
