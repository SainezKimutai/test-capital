from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.finish_form import FinishForm
from base.models.finish import Finish


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FinishCreateView(SuccessMessageMixin, CreateView):
    template_name = 'finish/finish_create.html'
    model = Finish
    form_class = FinishForm
    success_url = '/finish/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Finish '{form.instance.name}' successfully created!")
        return super().form_valid(form)


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

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        messages.success(self.request, f"Finish '{form.instance.name}' successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FinishDeleteView(DeleteView):
    template_name = 'finish/finish_confirm_delete.html'
    model = Finish
    success_url = '/finish/'


def finish_search(request):
    finish = Finish.objects.all()
    query = request.GET.get('q')
    if query:
        finish = Finish.objects.filter(
            Q(name__icontains=query)
        )
    paginator = Paginator(finish, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'finish': page_obj,
        'page_obj': page_obj,
        'query': query,
        'is_paginated': True
    }
    return render(request, 'finish/finish_list.html', context)
