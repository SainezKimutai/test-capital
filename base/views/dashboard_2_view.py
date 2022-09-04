import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from base.models.category import Category
from base.models.inventory import Inventory
from base.models.tag import Tag


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class Dashboard2(TemplateView):
    template_name = "dashboard/dashboard2.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Dashboard2, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(Dashboard2, self).get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        context["inventory"] = Inventory.objects.all()
        context["user"] = User.objects.all()
        context["tag"] = Tag.objects.all()
        context["chart_label_1"] = json.dumps(["January", "February", "March", "April", "May", "June", "July"])
        context["chart_data_1"] = json.dumps([
            {
                "label": "Electronics",
                "data": [30, 90, 43, 78, 33, 72, 88]
            },
            {
                "label": "Digital Goods",
                "data": [70, 10, 57, 27, 60, 22, 50]
            }
        ])
        context["chart_label_2"] = json.dumps(["2010", "2011", "2012", "2013", "2014", "2015", "2016"])
        context["chart_data_2"] = json.dumps([
            {
                "label": "Agriculture",
                "data": [88, 23, 40, 19, 86, 27, 90]
            },
            {
                "label": "Technology",
                "data": [50, 88, 33, 35, 53, 89, 40]
            },
            {
                "label": "Health",
                "data": [15, 23, 80, 45, 56, 55, 88]
            },
            {
                "label": "Business",
                "data": [37, 23, 35, 81, 55, 55, 40]
            }
        ])

        context['donut_label'] = json.dumps(['Chrome', 'IE', 'FireFox', 'Safari', 'Opera', 'Navigator'])
        context['donut_data'] = json.dumps([
            {
                "data": [700, 500, 400, 600, 300, 100],
                "backgroundColor": ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de'],
            }
        ])
        return context
