import calendar

from datetime import datetime, date, timedelta


def create_path(load_type: str, historical_date: date = None):
    if load_type == 'daily':
        today = datetime.today().date()
        return f'{today.year}/{today.month}/{today.day}/'
    elif load_type == 'historical':
        if not historical_date:
            raise ValueError("historical_date must be provided for historical load")
        try:
            return f'{historical_date.year}/{historical_date.month}/{historical_date.day}/'
        except ValueError as e:
            raise ValueError(f"Invalid historical_date format. Expected YYYY-MM-DD: {e}")
    else:
        raise ValueError(f"Invalid loading_type: {load_type}. Must be 'daily' or 'historical'")


def get_previous_month_dates() -> list[date]:
    today = date.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_prev_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_prev_month = last_day_of_prev_month.replace(day=1)
    num_days = calendar.monthrange(first_day_of_prev_month.year, first_day_of_prev_month.month)[1]
    return [first_day_of_prev_month + timedelta(days=i) for i in range(num_days)]
