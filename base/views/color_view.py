from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.color_form import ColorForm
from base.models.color import Color


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ColorCreateView(SuccessMessageMixin, CreateView):
    template_name = 'color/color_create.html'
    success_message = 'Color successfully created !'
    model = Color
    form_class = ColorForm
    success_url = '/color-create/'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ColorListView(ListView):
    template_name = 'color/color_list.html'
    model = Color
    context_object_name = 'color'
    paginate_by = 10


class ColorUpdateView(UpdateView):
    template_name = 'color/color_create.html'
    model = Color
    form_class = ColorForm
    success_url = '/color/'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ColorDeleteView(DeleteView):
    template_name = 'color/color_confirm_delete.html'
    model = Color
    success_url = '/color/'