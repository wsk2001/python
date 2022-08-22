from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def make_from_to(date_time_str, days=5):
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')

    from_date = date_time_obj - timedelta(days=days)
    to_date = date_time_obj + timedelta(days=days)

    str_from = from_date.strftime('%Y-%m-%d') 
    str_to = to_date.strftime('%Y-%m-%d') 

    return str_from, str_to



from_str, to_str = make_from_to('2022-02-19', 7)

print( 'from ', from_str )
print( 'to   ', to_str )
