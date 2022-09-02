from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.tag_form import TagForm
from base.models.tag import Tag


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TagCreateView(SuccessMessageMixin, CreateView):
    template_name = 'tag/tag_create.html'
    model = Tag
    form_class = TagForm
    success_url = '/tag/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Tag '{form.instance.name}' successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TagListView(ListView):
    template_name = 'tag/tag_list.html'
    model = Tag
    context_object_name = 'tag'


class TagUpdateView(UpdateView):
    template_name = 'tag/tag_create.html'
    model = Tag
    form_class = TagForm
    success_url = '/tag/'

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        messages.success(self.request, f"Tag '{form.instance.name}' successfully updated!")
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TagDeleteView(DeleteView):
    template_name = 'tag/tag_confirm_delete.html'
    model = Tag
    success_url = '/tag/'


def tag_search(request):
    tag = Tag.objects.all()
    query = request.GET.get('q')
    if query:
        tag = Tag.objects.filter(
            Q(name__icontains=query)
        )
    context = {
        'tag': tag,
        'query': query
    }
    return render(request, 'tag/tag_list.html', context)
