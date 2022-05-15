from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.range_form import RangeForm
from base.models.range import Range


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RangeCreateView(SuccessMessageMixin, CreateView):
    template_name = 'range/range_create.html'
    success_message = 'Range successfully created !'
    model = Range
    form_class = RangeForm
    success_url = '/range/'


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


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RangeDeleteView(DeleteView):
    template_name = 'range/range_confirm_delete.html'
    model = Range
    success_url = '/range/'