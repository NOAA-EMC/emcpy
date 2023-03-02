# coding: utf-8 -*-

"""
utilities for working with dates using datetime module (Python 2.3 or later)
original author: Jeff Whitaker <jeffrey.s.whitaker@noaa.gov>
"""

__all__ = [
    "dateto_hrs_since_day1CE",
    "hrs_since_day1CE_todate",
    "dateshift",
    "splitdate",
    "makedate",
    "hrstodate",
    "datetohrs",
    "daterange",
    "dayofyear",
    "getyrmon",
    "daysinmonth",
]

import datetime, calendar


hrsgregstart = 13865688  # hrs from 00010101 to 15821015 in Julian calendar.
# times in many datasets use mixed Gregorian/Julian calendar, datetime
# module uses a proleptic Gregorian calendar. So, I use datetime to compute
# hours since start of Greg. calendar (15821015) and add this constant to
# get hours since 1-Jan-0001 in the mixed Gregorian/Julian calendar.
gregstart = datetime.datetime(1582, 10, 15)  # datetime.datetime instance
day1 = datetime.datetime(1, 1, 1)  # datetime.datetime instance


def dateto_hrs_since_day1CE(curdate, mixedcal=True):
    """
    Given datetime.datetime instance, compute hours since 1-Jan-0001.
    Args:
        curdate: (datetime.datetime instance) date to check.
        mixedcal: (bool) is mixed Gregorian/Julian calendar used?

    Returns:
        hrs: (float) number of hours since 1-Jan-0001.
    """
    if mixedcal:
        if curdate < gregstart:
            msg = "date must be after start of gregorian calendar (15821015)!"
            raise ValueError(msg)
        difftime = curdate - gregstart
        hrsdiff = 24 * difftime.days + difftime.seconds / 3600
        hrs = hrsdiff + hrsgregstart
    else:
        difftime = curdate - day1
        hrs = 24.0 * (difftime.days + 1) + difftime.seconds / 3600.0
    return hrs


def hrs_since_day1CE_todate(hrs, mixedcal=True):
    """
    Return datetime.datetime instance given hours since 1-Jan-0001.
    Args:
        hrs: (float) number of hours since 1-Jan-0001 to compute a date.
        mixedcal: (bool) is mixed Gregorian/Julian calendar used?
    Returns:
        curdate: (datetime.datetime instance) date given hours since 1-Jan-0001.
    """
    if hrs < 0.0:
        msg = "hrs must be positive!"
        raise ValueError(msg)
    delta = datetime.timedelta(hours=1)
    if mixedcal:
        hrs_sincegreg = hrs - hrsgregstart
        curdate = gregstart + hrs_sincegreg * delta
    else:
        curdate = hrs * delta
    return curdate


def dateshift(analdate, fcsthr):
    """
    Compute verification date given analysis date string (yyyymmddhh) and fcst hour.
    Args:
        analdate: (date str) analysis date
        fcsthr: (int) forecast hour
    Returns:
        verifdate: (date str) verification date given analysis date string (yyyymmddhh) and fcst hour.
    """
    yyyy, mm, dd, hh = splitdate(analdate)
    analdate = datetime.datetime(yyyy, mm, dd, hh)
    verifdate = analdate + datetime.timedelta(hours=fcsthr)
    verifdate = makedate(verifdate.year, verifdate.month, verifdate.day, verifdate.hour)
    return verifdate


def splitdate(yyyymmddhh):
    """
    Given a date string (yyyymmddhh) return integers yyyy, mm, dd, and hh.
    Args:
        yyyymmddhh: (date str) date
    Returns:
        yyyy: (int) year
        mm: (int) month
        dd: (int) day
        hh: (int) hour
    """
    yyyy = int(yyyymmddhh[0:4])
    mm = int(yyyymmddhh[4:6])
    dd = int(yyyymmddhh[6:8])
    hh = int(yyyymmddhh[8:10])
    return yyyy, mm, dd, hh


def makedate(yyyy, mm, dd, hh):
    """
    Return a date string of the form yyyymmddhh given integers yyyy, mm, dd, and hh.
    Args:
        yyyy: (int) year
        mm: (int) month
        dd: (int) day
        hh: (int) hour
    Returns:
        yyyymmddhh: (date str) date string
    """
    yyyymmddhh = f"{yyyy}{mm:0>2}{dd:0>2}{hh:0>2}"
    return yyyymmddhh


def hrstodate(hrs, mixedcal=True):
    """
    Given number of hours since 1-Jan-0001, return date string.
    Args:
        hrs: (int) hours since
        mixedcal: (bool) is mixed Gregorian/Julian calendar used?
    Returns:
        yyyymmddhh: (date str) date string given hrs since day 1 CE.
    """
    date = hrs_since_day1CE_todate(hrs, mixedcal=mixedcal)
    yyyymmddhh = makedate(date.year, date.month, date.day, date.hour)
    return yyyymmddhh


def datetohrs(yyyymmddhh, mixedcal=True):
    """
    Given a date string, return number of hours since 1-Jan-0001.
    Args:
        yyyymmddhh: (date str) date to convert to hours since 1-Jan-0001.
        mixedcal: (bool) is mixed Gregorian/Julian calendar used?
    Returns:
        hrs_since_day1CE: (float) number of hours since day 1 CE.
    """
    yyyy, mm, dd, hh = splitdate(yyyymmddhh)
    hrs_since_day1CE = dateto_hrs_since_day1CE(datetime.datetime(yyyy, mm, dd, hh), mixedcal=mixedcal)
    return hrs_since_day1CE


def daterange(date1, date2, hrinc):
    """
    Return a list of date strings of the form yyyymmddhh given
    a starting date, ending date, and an increment in hours.
    Args:
        date1: (date str) start date
        date2: (date str) end date
        hrinc: (int) increment in hours
    Returns:
        dates: (list date str) of the form yyyymmddhh
    """
    date = date1
    delta = datetime.timedelta(hours=1)
    yyyy, mm, dd, hh = splitdate(date)
    d = datetime.datetime(yyyy, mm, dd, hh)
    n = 0
    dates = [date]
    while date < date2:
        d = d + hrinc * delta
        date = makedate(d.year, d.month, d.day, d.hour)
        dates.append(date)
        n = n + 1
    return dates


def dayofyear(yyyy, mm, dd):
    """
    Return the day number of the year given the year, month, and day.
    Args:
        yyyy: (int) year
        mm: (int) month
        dd: (int) day
        hh: (int) hour
    Returns:
        day_of_year: (int) day of year
    """
    d = datetime.datetime(yyyy, mm, dd)
    d0 = datetime.datetime(yyyy, 1, 1)
    day_of_year = int((d - d0).days)
    return day_of_year


def getyrmon(day_of_year, yyyy=2001):
    """
    Return the month and day given the day of the year and year.
    Args:
        day_of_year: (int) day of the year
        yyyy: (int) year
    Returns:
        mm: (int) month of year
        dd: (int) day of month
    """
    d1 = datetime.datetime(yyyy, 1, 1)
    if calendar.isleap(d1.year) and day_of_year > 366:
        raise ValueError("not that many days in the year")
    if not calendar.isleap(d1.year) and day_of_year > 365:
        raise ValueError("not that many days in the year")
    d2 = d1 + (day_of_year - 1) * datetime.timedelta(days=1)
    mm = d2.month
    dd = d2.day
    return mm, dd


def daysinmonth(yyyy, mm):
    """
    Return the number of days in a month given the year and month.
    Args:
        yyyy: (int) year
        mm: (int) month
    Returns:
        days_in_month: (int) number of days in month
    """
    days_in_month = calendar.monthrange(yyyy, mm)[1]
    return days_in_month


if __name__ == "__main__":
    print(dayofyear(2000, 2, 29))
    print(daysinmonth(2000, 2))
    print(datetohrs("0001010100", mixedcal=False))
    print(datetohrs("2001010100", mixedcal=False))
    print(datetohrs("2001010100", mixedcal=True))
