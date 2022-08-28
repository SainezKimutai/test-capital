from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from django.shortcuts import render

from base.utilities.helpers import format_period, format_string
from base.utilities.stats import  sales_report


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class ReportsView(TemplateView):
    template_name = "reports/reports.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReportsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)
        return context

    def get(self, request):
        template_name = "reports/reports.html"
        context = dict()
        return render(request, template_name, context)

    def post(self, request):
        template_name = "reports/reports.html"
        report_type = request.POST.get('report_type', None)
        report_interval = request.POST.get('report_interval', None)
        report_period = request.POST.get('report_period', None)
        context = dict()

        if report_type and report_interval and report_period:
            start_date, end_date = format_period(report_period)

            if format_string(report_type) == 'sales average':
                results = sales_report(report_interval, start_date, end_date)

            context['table'] = results['table']
            context['dataset'] = results['dataset']
            context['report_metric'] = results['report_metric']
            return render(request, template_name, context)

        else:
            return render(request, template_name, context)
