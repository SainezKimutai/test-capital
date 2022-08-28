from base.models.sales import SalesItem
from base.utilities.helpers import get_time_period_dates


def sales_report(interval, start_period, end_period):
    period_string, dates = get_time_period_dates(interval, start_period, end_period)
    table = []
    for index, date in enumerate(dates):
        start_date = date[0]
        end_date = date[1]
        data = {
            "period": f"{period_string} {index}",
            "from": start_date,
            "to": end_date,
            "value": SalesItem.objects.filter(created__range=[start_date, end_date]).count()
        }
        table.append(data)

    result = {
        'report_metric': 'Number Of Sales',
        'table': table,
        'dataset': []
    }

    return result
