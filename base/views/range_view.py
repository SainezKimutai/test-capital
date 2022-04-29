from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from base.forms.range_form import RangeForm
from base.models.range import Range


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateListRangeView(SuccessMessageMixin, CreateView, ListView):
    template_name = 'range/range_list.html'
    model = Range
    form_class = RangeForm
    success_message = "Range has been successfully created!"
    success_url = '/range/'
    context_object_name = 'range'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CreateListRangeView, self).get_context_data(**kwargs)
        range = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(range, self.paginate_by)

        try:
            range = paginator.page(page)
        except PageNotAnInteger:
            range = paginator.page(1)
        except EmptyPage:
            range = paginator.page(paginator.num_pages)
        context['range'] = range
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UpdateRangeView(UpdateView):
    template_name = 'range/range_list.html'
    model = Range
    form_class = RangeForm
    success_url = '/range/'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RangeDeleteView(DeleteView):
    template_name = 'range/range_confirm_delete.html'
    model = Range
    success_url = '/range/'
