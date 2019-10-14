import datetime


def format_date(date: datetime, d_format: str = '%Y%m%d') -> str:
    return datetime.datetime.strftime(date, d_format)


def format_delta(d_str: str, day_num: int = 0, d_format: str = '%Y%m%d') -> str:
    d: datetime = parse_str(d_str, d_format)
    return format_date(d + datetime.timedelta(days=day_num))


def get_current_dt() -> str:
    return format_date(datetime.datetime.now())


def parse_str(d_str: str, d_format: str = '%Y%m%d') -> datetime:
    return datetime.datetime.strptime(d_str, d_format)


def first_report_period(d_str: str, delta_year: int = 0) -> str:
    year_part = d_str[0:4]
    if delta_year != 0:
        year_int = int(year_part) + delta_year
        return '%d0331' % year_int
    else:
        return '%s0331' % year_part


def date_max(d_arr: list) -> str:
    ans = None
    for d_str in d_arr:
        if d_str is None:
            continue
        if ans is None or d_str > ans:
            ans = d_str
    return ans


def get_quarter_num(d_str: str) -> int:
    return (int(d_str[4:6]) - 1) // 3 + 1 if d_str is not None else None

def get_period(year: int, month: int) -> str:
    day = 30 if month == 6 or month == 9 else 31
    return '%d%02d%02d' % (year, month, day)

def next_period(d_str: str) -> str:
    year = int(d_str[0:4])
    month = int(d_str[4:6])
    if month == 12:
        year = year + 1
        month = 3
    else:
        month = month + 3
    return get_period(year, month)


def period_delta(d_str: str, delta: int) -> str:
    if delta == 0:
        return d_str
    year = int(d_str[0:4])
    month = int(d_str[4:6])
    step = 3
    if delta < 0:
        step = -3
        delta = abs(delta)
    for x in range(delta):
        month = month + step
        if month == 0:
            month = 12
            year = year - 1
        elif month == 15:
            month = 3
            year = year + 1
    return get_period(year, month)

