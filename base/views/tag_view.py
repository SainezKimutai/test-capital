from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.tag_form import TagForm
from base.models.tag import Tag


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TagCreateView(SuccessMessageMixin, CreateView):
    template_name = 'tag/tag_create.html'
    success_message = 'Tag successfully created !'
    model = Tag
    form_class = TagForm
    success_url = '/tag/'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TagListView(ListView):
    template_name = 'tag/tag_list.html'
    model = Tag
    context_object_name = 'tag'
    paginate_by = 10


class TagUpdateView(UpdateView):
    template_name = 'tag/tag_create.html'
    model = Tag
    form_class = TagForm
    success_url = '/tag/'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TagDeleteView(DeleteView):
    template_name = 'tag/tag_confirm_delete.html'
    model = Tag
    success_url = '/tag/'