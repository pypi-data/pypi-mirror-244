from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate(mode):
    current_date = datetime.now()
    current_time = current_date.strftime('%Y-%m-%d %H:%M:%S')
    today = current_date.strftime('%d_%m_%Y')
    one_month_ago = current_date - relativedelta(months=1)
    previous_month_year = one_month_ago.strftime("%m_%Y")
    current_month_year = today
    if mode == 'prev':
        return previous_month_year
    if mode == 'current':
        return current_month_year
    if mode == 'time':
        return current_time
    
def get_previous_month_year():
    previous_month_year = calculate('prev')
    previous_month_year = tuple(previous_month_year.split('_'))
    return previous_month_year

def get_current_month_year():
    current_month_year = calculate('current')
    current_month_year = tuple(current_month_year.split('_'))
    return current_month_year

def get_timestamp():
    return str(calculate('time'))


print(get_previous_month_year())
print(get_current_month_year())
print(get_timestamp())