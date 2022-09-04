from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from base.utilities.helpers import format_period, format_string
from base.utilities.reports import inventory_sales_report, sales_report


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

            if format_string(report_type) == 'sales_average':
                results = sales_report(report_interval, start_date, end_date)

            if format_string(report_type) == 'sales_per_inventory':
                results = inventory_sales_report(start_date, end_date)

            context['table'] = results['table']
            context['chart'] = results['chart']
            context['header_value'] = results['header_value']
            context['header_value_1'] = results['header_value_1']
            context['header_interval'] = results['header_interval']
            return render(request, template_name, context)

        else:
            return render(request, template_name, context)
