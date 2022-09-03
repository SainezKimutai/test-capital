import json

from django.db.models import Sum

from base.models.inventory import Inventory
from base.models.sales import SalesItem
from base.utilities.helpers import get_time_period_dates


def sales_report(interval, start_period, end_period):
    """ Number of sales report

    Args:
        interval (string): Interval
        start_period (date): Period start date
        end_period (date): Period end date

    Returns:
        dict: Results of table data, and chart data
    """
    period_string, dates = get_time_period_dates(interval, start_period, end_period)
    table_data = []
    chart_label = []
    chart_data = [
        {
            "label": "Number Of Sales",
            "data": []
        }
    ]
    for index, date in enumerate(dates):
        start_date = date[0]
        end_date = date[1]
        all_sales = SalesItem.objects.filter(
            created__gte=start_date,
            created__lte=end_date
        )

        all_count = all_sales.count()
        total_amount = all_sales.aggregate(Sum('total_amount'))
        data = {
            "index": index + 1,
            "from": start_date.strftime("%d %B %Y"),
            "to": end_date.strftime("%d %B %Y"),
            "value": all_count,
            "value_1": total_amount['total_amount__sum'] if total_amount['total_amount__sum'] else 0
        }

        table_data.append(data)
        chart_label.append(f"{period_string} {index + 1}")
        chart_data[0]["data"].append(all_count)

    result = {
        'header_value': 'Number Of Sales',
        'header_value_1': 'Total Amount',
        'header_interval': period_string,
        'table': table_data,
        'chart': {"label": json.dumps(chart_label), "data": json.dumps(chart_data)}
    }
    return result


def inventory_sales_report(start_period, end_period):
    """ Number of sales per inventory report

    Args:
        start_period (date): Period start date
        end_period (date): Period end date

    Returns:
        dict: Results of table data, and chart data
    """

    table_data = []
    chart_label = []
    chart_data = [
        {
            "label": "Number Of Sales",
            "data": []
        }
    ]
    all_inventories = Inventory.objects.all()
    for inventory in all_inventories:
        value_stat = SalesItem.objects.filter(inventory=inventory, created__range=[start_period, end_period]).count()
        data = {
            "index": inventory.name,
            "from": start_period.strftime("%d %B %Y"),
            "to": end_period.strftime("%d %B %Y"),
            "value": value_stat
        }

        table_data.append(data)
        chart_label.append(inventory.name)
        chart_data[0]["data"].append(value_stat)

    result = {
        'header_value': 'Number Of Sales',
        'header_value_1': None,
        'header_interval': "Inventories",
        'table': table_data,
        'chart': {"label": json.dumps(chart_label), "data": json.dumps(chart_data)}
    }
    return result
