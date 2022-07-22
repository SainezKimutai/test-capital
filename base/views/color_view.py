from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.color_form import ColorForm
from base.models.color import Color


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ColorCreateView(SuccessMessageMixin, CreateView):
    template_name = 'color/color_create.html'
    model = Color
    form_class = ColorForm
    success_url = '/color/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Color '{form.instance.name}' successfully created!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ColorListView(ListView):
    template_name = 'color/color_list.html'
    model = Color
    context_object_name = 'color'


class ColorUpdateView(UpdateView):
    template_name = 'color/color_create.html'
    model = Color
    form_class = ColorForm
    success_url = '/color/'

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        messages.success(self.request, f"Color '{form.instance.name}' successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ColorDeleteView(DeleteView):
    template_name = 'color/color_confirm_delete.html'
    model = Color
    success_url = '/color/'


def color_search(request):
    color = Color.objects.all()
    query = request.GET.get('q')
    if query:
        color = Color.objects.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query)
        )
    context = {
        'color': color,
        'query': query
    }
    return render(request, 'color/color_list.html', context)
