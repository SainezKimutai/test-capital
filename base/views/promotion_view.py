from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.promotion_form import PromotionForm
from base.models import Inventory, Promotion


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PromotionCreateView(SuccessMessageMixin, CreateView):
    template_name = 'promotion/promotion_create.html'
    model = Promotion
    form_class = PromotionForm
    success_url = '/promotion/'

    def get_context_data(self, **kwargs):
        context_data = super(PromotionCreateView, self).get_context_data(**kwargs)
        context_data['Inventories'] = Inventory.objects.all()
        context_data['test'] = True
        return context_data

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Promotion was successfully created!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PromotionListView(ListView):
    template_name = 'promotion/promotion_list.html'
    model = Promotion
    context_object_name = 'promotions'


class PromotionUpdateView(UpdateView):
    template_name = 'promotion/promotion_create.html'
    model = Promotion
    form_class = PromotionForm
    success_url = '/promotion/'

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        messages.success(self.request, "Promotion was successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PromotionDeleteView(DeleteView):
    template_name = 'promotion/promotion_delete.html'
    model = Promotion
    success_url = '/promotion/'


def promotion_search(request):
    promotions = Promotion.objects.all()
    query = request.GET.get('q')
    if query:
        promotions = Promotion.objects.filter(
            Q(promotion_price__icontains=query) |
            Q(description__icontains=query) |
            Q(inventory__name__icontains=query)
        )
    context = {
        'promotions': promotions,
        'query': query
    }
    return render(request, 'promotion/promotion_list.html', context)
