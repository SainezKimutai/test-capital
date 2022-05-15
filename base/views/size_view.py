from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.size_form import SizeForm
from base.models.size import Size


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SizeCreateView(SuccessMessageMixin, CreateView):
    template_name = 'size/size_create.html'
    success_message = 'Size successfully created !'
    model = Size
    form_class = SizeForm
    success_url = '/size/'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SizeListView(ListView):
    template_name = 'size/size_list.html'
    model = Size
    context_object_name = 'size'
    paginate_by = 10


class SizeUpdateView(UpdateView):
    template_name = 'size/size_create.html'
    model = Size
    form_class = SizeForm
    success_url = '/size/'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SizeDeleteView(DeleteView):
    template_name = 'size/size_confirm_delete.html'
    model = Size
    success_url = '/size/'