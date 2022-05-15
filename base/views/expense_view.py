
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from base.forms.expense_form import ExpenseForm
from base.models.expense import Expense


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateExpenseView(SuccessMessageMixin, CreateView):
    template_name = 'expense/create_expense.html'
    model = Expense
    form_class = ExpenseForm
    success_url = '/expense/'

    def get_success_message(self, cleaned_data):
        return f"Expense requested by {self.object.requester} was successfully created!!"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ExpenseListView(ListView):
    template_name = 'expense/expense_list.html'
    model = Expense
    context_object_name = 'expense'
    paginate_by = 10


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ExpenseDetailView(DetailView):
    template_name = 'expense/expense_details.html'
    model = Expense
    context_object_name = 'expense'


class ExpenseUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'expense/create_expense.html'
    model = Expense
    form_class = ExpenseForm
    success_url = '/expense/'

    def get_success_message(self, cleaned_data):
        return f"Expense requested by {self.object.requester} was successfully updated!!"

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


def expense_search(request):
    expense = Expense.objects.all()
    query = request.GET.get('q')
    if query:
        expense = Expense.objects.filter(
            Q(description__icontains=query) |
            Q(amount__icontains=query) |
            Q(requester__username__icontains=query)
        )
    context = {
        'expense': expense,
        'query': query
    }

    return render(request, 'expense/expense_list.html', context)
