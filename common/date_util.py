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


def get_bus_month_end(year, month):
    month_end = get_month_end(year, month)
    while not is_bus_day(month_end):
        month_end = month_end - timedelta(days=1)
    return month_end


if __name__ == "__main__":
    print(get_bus_month_end(2023, 4))
    print(datetime.combine(date(1999, 5, 31), datetime.min.time()) in get_holidays(date(1999, 5, 31).year))
    print(get_bus_month_end(1999, 5))
    print(get_holidays(2002))