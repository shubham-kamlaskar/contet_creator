from datetime import datetime, date

def get_current_dt_in_milliseconds_precision():
    return datetime.now()

def calculate_difference_between_dates(past_date: date):
    current_date = get_current_dt_in_milliseconds_precision().date()
    diff = current_date - past_date
    return diff.days