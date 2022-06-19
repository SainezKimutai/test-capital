from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from base.forms.credit_note_form import CreditNoteForm
from base.models.credit_note import CreditNote
from base.models.sales import SalesItem


@login_required
def create_credit_note_view(request, pk):
    sale_item = SalesItem.objects.get(id=pk)
    form = CreditNoteForm(request.POST or None, initial={"sales_item": sale_item, "quantity": sale_item.quantity})
    if request.method == 'POST':

        if form.is_valid():
            credit_note = form.save()
            credit_note.created_by = request.user
            credit_note.save()
            messages.add_message(request, messages.SUCCESS,
                                 f'Credit note successfully created for sale item {credit_note.sales_item}, '
                                 f'quantity {credit_note.quantity}')
            return redirect('sale_item_information')
    return render(request, 'credit_note/credit_note_information.html', context={'form': form})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreditNoteListView(ListView):
    template_name = 'credit_note/credit_note_list.html'
    model = CreditNote
    context_object_name = 'credit_note'
    paginate_by = 10


def credit_note_search(request):
    credit_note = CreditNote.objects.all()
    query = request.GET.get('q')
    if query:
        credit_note = CreditNote.objects.filter(
            Q(sales_item__sales_order__customer__name__icontains=query) |
            Q(sales_item__sales_order__sales_agent__username__icontains=query) |
            Q(sales_item__sales_order__sales_agent__first_name__icontains=query) |
            Q(sales_item__sales_order__sales_agent__last_name__icontains=query) |
            Q(sales_item__sales_order__receipt_number__icontains=query) |
            Q(sales_item__inventory__name__icontains=query) |
            Q(sales_item__sales_order__transaction_type__icontains=query)
        )
    context = {
        'credit_note': credit_note,
        'query': query
    }
    return render(request, 'credit_note/credit_note_list.html', context)
