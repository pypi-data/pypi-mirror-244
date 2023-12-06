from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate(mode):
    current_date = datetime.now()
    current_time = current_date.strftime('%Y-%m-%d %H:%M:%S')
    current_month_year = current_date.strftime('%Y_%m_%d')
    one_month_ago = current_date - relativedelta(months=1)
    previous_month_year = one_month_ago.strftime("%Y_%m")
    if mode == 'prev':
        return previous_month_year.split('_')
    if mode == 'current':
        return current_month_year.split('_')
    if mode == 'time':
        return current_time

def get_previous_month_year() -> dict:
    previous_month_year = calculate('prev')
    year = previous_month_year[0]
    month = previous_month_year[1]
    previous = {
        'year' : year,
        'month' : month
    }
    return previous

def get_current_month_year() -> dict:
    current_month_year = calculate('current')
    year = current_month_year[0]
    month = current_month_year[1]
    day = current_month_year[2]
    current = {
        'day' : day,
        'month' : month,
        'year' : year
    }
    return current

def get_timestamp() -> str:
    return str(calculate('time'))