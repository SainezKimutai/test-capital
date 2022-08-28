import datetime


def format_period(period):
    """ Convert string of dates to date type

    Args:
        period (string): Date string like "1, 05, 2022 - 31, 08, 2022"

    Returns:
        datetime: Return start date and snd date
    """
    start_date_str = period.split('-')[0]
    end_date_str = period.split('-')[1]

    start_date_day = int(start_date_str.split(',')[0])
    start_date_month = int(start_date_str.split(',')[1])
    start_date_year = int(start_date_str.split(',')[2])

    end_date_day = int(end_date_str.split(',')[0])
    end_date_month = int(end_date_str.split(',')[1])
    end_date_year = int(end_date_str.split(',')[2])

    formated_start_date = datetime.datetime(start_date_year, start_date_month, start_date_day)
    formated_end_date = datetime.datetime(end_date_year, end_date_month, end_date_day)

    return formated_start_date, formated_end_date


def format_string(text):
    """ Remove leading and trailing whitespaces in a string, and return in lower case """
    return text.strip().lower()


def get_time_period_dates(interval, period_start_date, period_end_date):
    if format_string(interval) == 'weekly':
        period_string = 'Week'
        end_date = period_start_date
        loop = True
        dates = []
        while loop:
            start_date = end_date
            end_date += datetime.timedelta(days=7)

            if end_date > period_end_date:
                loop = False
                end_date = period_end_date

            dates.append([start_date, end_date])
        return period_string, dates
