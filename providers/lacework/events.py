from . import lw
from . import datetime_to_lacework_time

def events(start_time, end_time):
    return lw.events.get_for_date_range(start_time=datetime_to_lacework_time(start_time), end_time=datetime_to_lacework_time(end_time))
