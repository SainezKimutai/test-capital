from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.range_form import RangeForm
from base.models.range import Range


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RangeCreateView(SuccessMessageMixin, CreateView):
    template_name = 'range/range_create.html'
    model = Range
    form_class = RangeForm
    success_url = '/range/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Range '{form.instance.name}' successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RangeListView(ListView):
    template_name = 'range/range_list.html'
    model = Range
    context_object_name = 'range'
    paginate_by = 10


class RangeUpdateView(UpdateView):
    template_name = 'range/range_create.html'
    model = Range
    form_class = RangeForm
    success_url = '/range/'

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        messages.success(self.request, f"Range '{form.instance.name}' successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RangeDeleteView(DeleteView):
    template_name = 'range/range_confirm_delete.html'
    model = Range
    success_url = '/range/'


def range_search(request):
    range = Range.objects.all()
    query = request.GET.get('q')
    if query:
        range = Range.objects.filter(
            Q(name__icontains=query)
        )
    context = {
        'range': range,
        'query': query
    }
    return render(request, 'range/range_list.html', context)
