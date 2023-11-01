import calendar
import numpy as np
from datetime import date, datetime, timedelta
from dateutil import rrule, easter
from pandas.tseries.holiday import USFederalHolidayCalendar


def get_month_end(year, month):
    return date(year, month, calendar.monthrange(year, month)[1])


def get_holidays(year):
    cal = USFederalHolidayCalendar()
    federal_holidays = cal.holidays(start=date(year, 1, 1).strftime("%Y-%m-%d"), end=date(year, 12, 31).strftime("%Y-%m-%d")).to_pydatetime()
    federal_holidays = np.append(federal_holidays, datetime.combine(easter.easter(year)+timedelta(days=-2), datetime.min.time()))
    return federal_holidays


def is_bus_day(dt):
    return dt.weekday() < 5 and (datetime.combine(dt, datetime.min.time()) not in get_holidays(dt.year))


def get_bus_date(dt):
    while not is_bus_day(dt):
        dt = dt + timedelta(days=1)
    return dt


def get_bus_month_end(year, month):
    month_end = get_month_end(year, month)
    while not is_bus_day(month_end):
        month_end = month_end - timedelta(days=1)
    return month_end


def get_previous_month_end(as_of_date):
    i = as_of_date.year - 1 if as_of_date.month == 1 else as_of_date.year
    j =  12 if as_of_date.month == 1 else as_of_date.month - 1
    return get_bus_month_end(i, j)


def get_previous_quarter_end(as_of_date):
    i = as_of_date.year - 1 if as_of_date.month <= 3 else as_of_date.year
    j = as_of_date.month + 9 if as_of_date.month <= 3 else as_of_date.month - 3
    return get_bus_month_end(i, j)


def get_next_rebal_day(as_of_date, day_of_week=3):
    rebal_date = as_of_date + timedelta(days=7 + day_of_week - (as_of_date.weekday() + 1))
    while not is_bus_day(rebal_date):
        rebal_date = rebal_date + timedelta(days=1)
    return rebal_date


if __name__ == "__main__":
    print(get_bus_month_end(2023, 4))
    print(datetime.combine(date(1999, 5, 31), datetime.min.time()) in get_holidays(date(1999, 5, 31).year))
    print(get_bus_month_end(1999, 5))
    print(get_holidays(2002))
    print(get_previous_quarter_end(get_bus_month_end(1999, 5)))
    as_of_date = date(1999, 1, 1)
    while as_of_date <= date(2010, 12, 31):
        rebal_date = get_next_rebal_day(as_of_date, 3)
        print(rebal_date)
        as_of_date = rebal_date
