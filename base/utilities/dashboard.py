import json
from datetime import datetime

from django.db.models import Sum

from dateutil.relativedelta import relativedelta

from base.models.inventory import Inventory
from base.models.sales import SalesItem


def get_sales_chart_data(months=4):
    """Sales report on count and amount

    Args:
        months (int, optional): Number of months report on. Defaults to 4.

    Returns:
        dict: Chart data with label and dataset
    """
    chart_label = []
    chart_count = [
        {
            "label": "Number Of Sales",
            "data": []
        }
    ]
    chart_amount = [
        {
            "label": "Sales Amount",
            "data": []
        }
    ]
    start_date = datetime.now()
    for _ in range(months):

        end_date = start_date - relativedelta(months=1)

        all_sales = SalesItem.objects.filter(
            created__lte=start_date,
            created__gte=end_date
        )

        all_count = all_sales.count()
        total_sum = all_sales.aggregate(Sum('total_amount'))
        total_amount = total_sum['total_amount__sum'] if total_sum['total_amount__sum'] else 0
        chart_label.append(f'{start_date.strftime("%d %B")} - {end_date.strftime("%d %B")}')
        chart_count[0]["data"].append(all_count)
        chart_amount[0]["data"].append(int(total_amount))

        start_date = end_date

    result = {
        "label": json.dumps(chart_label),
        "count_data": json.dumps(chart_count),
        "amount_data": json.dumps(chart_amount),
    }
    return result


def get_inventory_chart_data(months=2, top=4):
    """Inventory Sales report on count and amount

    Args:
        months (int, optional): Number of months report on. Defaults to 4.

    Returns:
        dict: Chart data with label and dataset
    """
    chart_label_count = []
    chart_label_amount = []
    chart_count = [
        {
            "label": "Inventory count",
            "data": [],
            "backgroundColor": ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de']
        }
    ]
    chart_amount = [
        {
            "label": "Inventory Amount",
            "data": [],
            "backgroundColor": ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de']
        }
    ]
    start_date = datetime.now()

    end_date = start_date - relativedelta(months=months)

    all_inventories = Inventory.objects.all()

    unsorted_inventories = []
    for inventory in all_inventories:

        all_sales = SalesItem.objects.filter(
            inventory=inventory,
            created__lte=start_date,
            created__gte=end_date
        )

        all_count = all_sales.count()
        total_sum = all_sales.aggregate(Sum('total_amount'))
        total_amount = total_sum['total_amount__sum'] if total_sum['total_amount__sum'] else 0

        unsorted_inventories.append({
            "name": inventory.name,
            "count": all_count,
            "amount": int(total_amount)
        })

    sorted_count = sorted(unsorted_inventories, key=lambda kv: kv["count"], reverse=True)[:top]
    sorted_amount = sorted(unsorted_inventories, key=lambda kv: kv["amount"], reverse=True)[:top]

    for item in sorted_count:
        chart_label_count.append(f'{item["name"]}')
        chart_count[0]["data"].append(item["count"])

    for item in sorted_amount:
        chart_label_amount.append(f'{item["name"]}')
        chart_amount[0]["data"].append(item["amount"])

    result = {
        "label_count": json.dumps(chart_label_count),
        "label_amount": json.dumps(chart_label_amount),
        "count_data": json.dumps(chart_count),
        "amount_data": json.dumps(chart_amount)
    }
    return result
