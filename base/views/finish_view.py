from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.finish_form import FinishForm
from base.models.finish import Finish


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FinishCreateView(SuccessMessageMixin, CreateView):
    template_name = 'finish/finish_create.html'
    success_message = 'Finish successfully created !'
    model = Finish
    form_class = FinishForm
    success_url = '/finish/'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FinishListView(ListView):
    template_name = 'finish/finish_list.html'
    model = Finish
    context_object_name = 'finish'
    paginate_by = 10


class FinishUpdateView(UpdateView):
    template_name = 'finish/finish_create.html'
    model = Finish
    form_class = FinishForm
    success_url = '/finish/'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FinishDeleteView(DeleteView):
    template_name = 'finish/finish_confirm_delete.html'
    model = Finish
    success_url = '/finish/'