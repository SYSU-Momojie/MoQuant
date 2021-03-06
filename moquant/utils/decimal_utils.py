import math
from decimal import Decimal

from moquant.utils.compare_utils import mini, maxi


def add(*args):
    result = Decimal(0)
    for num in args:
        to_add = none_to_zero(num)
        if isinstance(to_add, Decimal):
            result += to_add
        else:
            result += Decimal(to_add)
    return result


def sub(a, *args):
    result = add(a)
    for num in args:
        to_sub = none_to_zero(num)
        if isinstance(to_sub, Decimal):
            result -= to_sub
        else:
            result -= Decimal(to_sub)
    return result


def mul(a, b, err_default=0):
    if a is None or b is None or math.isnan(a) or math.isnan(b):
        return Decimal(err_default) if err_default is not None else None
    if not isinstance(a, Decimal):
        a = Decimal(a)
    if not isinstance(b, Decimal):
        b = Decimal(b)
    return a * b


def div(a, b, err_default=0):
    if a is None or b is None or b == 0:
        return Decimal(err_default) if err_default is not None else None
    if not isinstance(a, Decimal):
        a = Decimal(a)
    if not isinstance(b, Decimal):
        b = Decimal(b)
    return a / b


def yoy(current, last_year, err_default=None):
    if current is None or last_year is None or last_year == 0:
        return Decimal(err_default) if err_default is not None else None
    else:
        return (current - last_year) / abs(last_year)


def valid_score(score, s=0, e=100):
    return mini(maxi(score, s), e)


def avg_in_exists(*args):
    total = Decimal(0)
    count = Decimal(0)
    for num in args:
        if num is None:
            continue
        if isinstance(num, Decimal):
            total += num
        else:
            total += Decimal(num)
        count += 1
    return div(total, count)


def cut_format(num: Decimal):
    if num is None:
        return '0'
    elif not isinstance(num, Decimal):
        num = Decimal(num)
    if num >= 100:
        return num.quantize(Decimal('0.0'))
    else:
        return num.quantize(Decimal('0.00'))


def unit_format(num):
    if num is None:
        return '0'
    elif not isinstance(num, Decimal):
        num = Decimal(num)
    abs_val = num.copy_abs()
    if abs_val >= pow(10, 8):
        return '%s亿' % cut_format(div(num, pow(10, 8)))
    elif abs_val >= pow(10, 4):
        return '%s万' % cut_format(div(num, pow(10, 4)))
    else:
        return '%s' % cut_format(num)


def percent_format(num):
    if num is None:
        num = 0
    if not isinstance(num, Decimal):
        num = Decimal(num)
    return '%s%%' % cut_format(num * 100)


def none_to_zero(num):
    if num is None or math.isnan(num):
        return 0
    else:
        return num


def negative(num):
    if num is None or math.isnan(num):
        return 0
    else:
        return num * (-1)


def equals(a: Decimal, b: Decimal) -> bool:
    """
    判断两个数是否相等，相差1e-9以内即可
    :param a:
    :param b:
    :return: 是否精度内相等
    """
    if a is None and b is None:
        return True
    elif a is None:
        return False
    elif b is None:
        return False
    else:
        return abs(a - b) < 1e-9


def cal_qfq(ori: Decimal, now_adj: Decimal, latest_ajd: Decimal) -> Decimal:
    """
    根据复权因子计算前复权价格，复权因子相等则不计算避免误差出现
    :param ori: 原来的值
    :param now_adj: 当天的复权因子
    :param latest_ajd: 最新的复权因子
    :return: 前复权价格
    """
    return ori if equals(now_adj, latest_ajd) else \
        div(mul(ori, now_adj), latest_ajd).quantize(Decimal('1.00'), rounding='ROUND_UP')
