from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView

from base.forms.replenishment_form import (
    ReplenishmentForm, ReplenishmentItemInlineFormset
)
from base.helper import generate_receipt
from base.models import Inventory, Replenishment


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ReplenishmentCreateView(CreateView):
    form_class = ReplenishmentForm
    template_name = 'replenishment/replenishment_create.html'
    success_url = '/replenishment/'

    def get_context_data(self, **kwargs):
        context = super(ReplenishmentCreateView, self).get_context_data(**kwargs)

        context['replenishment_item_formset'] = ReplenishmentItemInlineFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        replenishment_item_formset = ReplenishmentItemInlineFormset(self.request.POST)
        if form.is_valid() and replenishment_item_formset.is_valid():
            return self.form_valid(form, replenishment_item_formset)
        else:
            return self.form_invalid(form, replenishment_item_formset)

    def form_valid(self, form, replenishment_item_formset):
        form.instance.receipt_number = generate_receipt(Replenishment, 'RPL')
        form.instance.created_by = self.request.user
        form.instance.total_amount = 0
        self.object = form.save()
        # saving ReplenishmentItem Instances
        replenishment_items = replenishment_item_formset.save(commit=False)
        for item in replenishment_items:
            item.replenishment = self.object
            item.save()
            # Update Inventory
            inventory = Inventory.objects.get(id=item.inventory.id)
            inventory.current_stock += item.count
            inventory.save()

            self.object.total_amount += item.amount

        self.object.save()
        messages.success(self.request, f"Replenishment '{self.object.receipt_number}' was successfully created!")

        return redirect(reverse("replenishment_list"))

    def form_invalid(self, form, replenishment_item_formset):

        return self.render_to_response(
            self.get_context_data(form=form,
                                  replenishment_item_formset=replenishment_item_formset
                                  )
        )


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


def replenishment_search(request):
    replenishments = Replenishment.objects.all()
    query = request.GET.get('q')
    if query:
        replenishments = Replenishment.objects.filter(
            Q(receipt_number__icontains=query)
        )
    context = {
        'replenishments': replenishments,
        'query': query
    }
    return render(request, 'replenishment/replenishment_list.html', context)
