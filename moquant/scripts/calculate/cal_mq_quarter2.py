import sys
import time
from decimal import Decimal
from functools import partial

from sqlalchemy.orm import Session

from moquant.constants import mq_calculate_start_date, mq_report_type, mq_quarter_indicator_enum
from moquant.dbclient import db_client, mq_quarter_indicator
from moquant.dbclient.mq_forecast_agg import MqForecastAgg
from moquant.dbclient.mq_quarter_indicator import MqQuarterIndicator
from moquant.dbclient.mq_stock_mark import MqStockMark
from moquant.dbclient.ts_balance_sheet import TsBalanceSheet
from moquant.dbclient.ts_cashflow import TsCashFlow
from moquant.dbclient.ts_dividend import TsDividend
from moquant.dbclient.ts_fina_indicator import TsFinaIndicator
from moquant.dbclient.ts_income import TsIncome
from moquant.log import get_logger
from moquant.service.mq_quarter_store import MqQuarterStore, init_quarter_store
from moquant.utils import decimal_utils
from moquant.utils.date_utils import format_delta, get_current_dt, period_delta, get_quarter_num

log = get_logger(__name__)


def ready_data(ts_code: str, from_date: str):
    session: Session = db_client.get_session()
    income_arr = session.query(TsIncome) \
        .filter(
        TsIncome.ts_code == ts_code, TsIncome.mq_ann_date >= from_date, TsIncome.report_type == 1) \
        .order_by(TsIncome.mq_ann_date.asc(), TsIncome.end_date.asc()).all()

    adjust_income_arr = session.query(TsIncome) \
        .filter(
        TsIncome.ts_code == ts_code, TsIncome.mq_ann_date >= from_date, TsIncome.report_type == 4) \
        .order_by(TsIncome.mq_ann_date.asc(), TsIncome.end_date.asc()).all()

    balance_arr = session.query(TsBalanceSheet) \
        .filter(TsBalanceSheet.ts_code == ts_code, TsBalanceSheet.mq_ann_date >= from_date,
                TsBalanceSheet.report_type == 1) \
        .order_by(TsBalanceSheet.mq_ann_date.asc(), TsBalanceSheet.end_date.asc()).all()

    adjust_balance_arr = session.query(TsBalanceSheet) \
        .filter(TsBalanceSheet.ts_code == ts_code, TsBalanceSheet.mq_ann_date >= from_date,
                TsBalanceSheet.report_type == 4) \
        .order_by(TsBalanceSheet.mq_ann_date.asc(), TsBalanceSheet.end_date.asc()).all()

    cash_arr = session.query(TsCashFlow) \
        .filter(TsCashFlow.ts_code == ts_code, TsCashFlow.mq_ann_date >= from_date,
                TsCashFlow.report_type == 1) \
        .order_by(TsCashFlow.mq_ann_date.asc(), TsCashFlow.end_date.asc()).all()

    adjust_cash_arr = session.query(TsCashFlow) \
        .filter(TsCashFlow.ts_code == ts_code, TsCashFlow.mq_ann_date >= from_date,
                TsCashFlow.report_type == 4) \
        .order_by(TsCashFlow.mq_ann_date.asc(), TsCashFlow.end_date.asc()).all()

    fina_arr = session.query(TsFinaIndicator) \
        .filter(TsFinaIndicator.ts_code == ts_code, TsFinaIndicator.ann_date >= from_date,
                TsFinaIndicator.ann_date != None) \
        .order_by(TsFinaIndicator.ann_date.asc(), TsFinaIndicator.end_date.asc()).all()

    dividend_arr = session.query(TsDividend) \
        .filter(TsDividend.ts_code == ts_code, TsDividend.ann_date >= from_date, TsDividend.div_proc == '实施') \
        .order_by(TsDividend.ann_date.asc()).all()

    forecast_arr = session.query(MqForecastAgg) \
        .filter(MqForecastAgg.ts_code == ts_code, MqForecastAgg.ann_date >= from_date) \
        .order_by(MqForecastAgg.ann_date.asc(), MqForecastAgg.end_date.asc()).all()

    session.close()
    return income_arr, adjust_income_arr, balance_arr, adjust_balance_arr, cash_arr, adjust_cash_arr, \
           fina_arr, dividend_arr, forecast_arr


def fit_update_date(date: str, arr: list, field_name: str) -> bool:
    if len(arr) == 0:
        return False
    target_date = getattr(arr[0], field_name)
    return target_date is not None and target_date == format_delta(date, 1)


def common_add(result_list: list, store: MqQuarterStore, to_add: MqQuarterIndicator):
    store.add(to_add)
    result_list.append(to_add)


def common_log_err(ts_code: str, period: str, update_date: str, name: str):
    log.error('Fail to cal %s of %s, period: %s, date: %s' % (name, ts_code, period, update_date))


def add_nx(ts_code: str, report_type: int, period: str, update_date: str,
           name: str, value: Decimal,
           result_list: list, store: MqQuarterStore, period_set: set):
    if value is None:
        return
    exist = store.find_period_latest(ts_code, name, period)
    if exist is not None and exist.update_date == update_date:
        return
    to_add = MqQuarterIndicator(ts_code=ts_code, report_type=(1 << report_type), period=period, update_date=update_date,
                                name=name, value=value)
    common_add(result_list, store, to_add)
    period_set.add(period)


def extract_from_forecast(result_list: list, store: MqQuarterStore, period_set: set, forecast: MqForecastAgg):
    call_add_nx = partial(
        add_nx, ts_code=forecast.ts_code, period=forecast.end_date, update_date=format_delta(forecast.ann_date, -1),
        report_type=mq_report_type.forecast,
        store=store, result_list=result_list, period_set=period_set
    )

    for i in mq_quarter_indicator_enum.extract_from_forecast_list:
        call_add_nx(name=i.name, value=getattr(forecast, i.from_name))


def extract_from_income(result_list: list, store: MqQuarterStore, period_set: set, income: TsIncome):
    call_add_nx = partial(
        add_nx, ts_code=income.ts_code, period=income.end_date, update_date=format_delta(income.mq_ann_date, -1),
        report_type=mq_report_type.report if income.report_type == 1 else mq_report_type.report_adjust,
        store=store, result_list=result_list, period_set=period_set
    )
    for i in mq_quarter_indicator_enum.extract_from_income_list:
        call_add_nx(name=i.name, value=getattr(income, i.from_name))


def extract_from_balance(result_list: list, store: MqQuarterStore, period_set: set, bs: TsBalanceSheet):
    call_add_nx = partial(
        add_nx, ts_code=bs.ts_code, period=bs.end_date, update_date=format_delta(bs.mq_ann_date, -1),
        report_type=mq_report_type.report if bs.report_type == 1 else mq_report_type.report_adjust,
        store=store, result_list=result_list, period_set=period_set
    )

    for i in mq_quarter_indicator_enum.extract_from_bs_list:
        call_add_nx(name=i.name, value=getattr(bs, i.from_name))


def extract_from_cash_flow(result_list: list, store: MqQuarterStore, period_set: set, cf: TsCashFlow):
    call_add_nx = partial(
        add_nx, ts_code=cf.ts_code, period=cf.end_date, update_date=format_delta(cf.mq_ann_date, -1),
        report_type=mq_report_type.report if cf.report_type == 1 else mq_report_type.report_adjust,
        store=store, result_list=result_list, period_set=period_set
    )

    for i in mq_quarter_indicator_enum.extract_from_cf_list:
        call_add_nx(name=i.name, value=getattr(cf, i.from_name))


def extract_from_fina_indicator(result_list: list, store: MqQuarterStore, period_set: set, fina: TsFinaIndicator):
    call_add_nx = partial(
        add_nx, ts_code=fina.ts_code, period=fina.end_date, update_date=format_delta(fina.ann_date, -1),
        report_type=mq_report_type.report,
        store=store, result_list=result_list, period_set=period_set
    )

    for i in mq_quarter_indicator_enum.extract_from_fi_list:
        call_add_nx(name=i.name, value=getattr(fina, i.from_name))


def extract_from_dividend(result_list: list, store: MqQuarterStore, period_set: set, d: TsDividend):
    call_add_nx = partial(
        add_nx, ts_code=d.ts_code, period=d.end_date, update_date=format_delta(d.imp_ann_date, -1),
        report_type=mq_report_type.report,
        store=store, result_list=result_list, period_set=period_set
    )

    dividend = decimal_utils.mul(d.cash_div_tax * d.base_share)
    call_add_nx(name='dividend', value=dividend)


def copy_indicator_from_latest(result_list: list, store: MqQuarterStore, period: str, ts_code: str, update_date: str,
                               name: str):
    i = store.find_period_latest(ts_code, name, period)
    if i is None or i.update_date == update_date:
        return
    ni = MqQuarterIndicator(ts_code=i.ts_code, report_type=i.report_type, period=i.period, update_date=update_date,
                            name=i.name, value=i.value)
    common_add(result_list, store, ni)


def copy_from_latest(result_list: list, store: MqQuarterStore, period_set: set, ts_code: str, update_date: str):
    call_copy = partial(copy_indicator_from_latest, result_list=result_list, store=store,
                        ts_code=ts_code, update_date=update_date)
    period_list = list(period_set)
    period_list.sort()
    for period in period_list:
        for i in mq_quarter_indicator_enum.extract_from_income_list:
            call_copy(period=period, name=i.name)
        for i in mq_quarter_indicator_enum.extract_from_bs_list:
            call_copy(period=period, name=i.name)
        for i in mq_quarter_indicator_enum.extract_from_cf_list:
            call_copy(period=period, name=i.name)
        for i in mq_quarter_indicator_enum.extract_from_fi_list:
            call_copy(period=period, name=i.name)
        for i in mq_quarter_indicator_enum.extract_from_forecast_list:
            call_copy(period=period, name=i.name)

        call_copy(period=period, name='dividend')


def fill_empty(result_list: list, store: MqQuarterStore, period_set: set, ts_code: str, update_date: str):
    period_list = list(period_set)
    period_list.sort()
    for period in period_list:
        for i in mq_quarter_indicator_enum.fill_empty_list:
            exist = store.find_period_latest(ts_code, i.name, period)
            if exist is None:
                to_add = MqQuarterIndicator(ts_code=ts_code, report_type=mq_report_type.report,
                                            period=period, update_date=update_date,
                                            name=i.name, value=Decimal(0))
                common_add(result_list, store, to_add)


def cal_ltm(result_list: list, store: MqQuarterStore, period: str, ts_code: str, update_date: str):
    call_find_now = partial(store.find_period_exact, ts_code=ts_code, update_date=update_date)
    call_find_pre = partial(store.find_period_latest, ts_code=ts_code)
    call_add = partial(common_add, result_list=result_list, store=store)

    for k in mq_quarter_indicator_enum.cal_quarter_list:
        name = k.name
        from_name = k.from_name
        i1 = call_find_now(period=period, name=from_name)
        i2 = call_find_pre(period=period_delta(period, -1), name=from_name)
        quarter = mq_quarter_indicator.cal_quarter(name, i1, i2)
        if quarter is None:
            common_log_err(ts_code, period, update_date, name)
        else:
            call_add(to_add=quarter)

    for k in mq_quarter_indicator_enum.cal_ltm_list:
        name = k.name
        from_name = k.from_name
        i1 = call_find_now(period=period, name=from_name)
        i2 = call_find_pre(period=period_delta(period, -1), name=from_name)
        i3 = call_find_pre(period=period_delta(period, -2), name=from_name)
        i4 = call_find_pre(period=period_delta(period, -3), name=from_name)
        ltm = mq_quarter_indicator.cal_ltm(name, i1, i2, i3, i4)
        if ltm is None:
            common_log_err(ts_code, period, update_date, name)
        else:
            call_add(to_add=ltm)


def cal_avg(result_list: list, store: MqQuarterStore, period: str, ts_code: str, update_date: str):
    call_find_now = partial(store.find_period_exact, ts_code=ts_code, update_date=update_date)
    call_find_pre = partial(store.find_period_latest, ts_code=ts_code)
    call_add = partial(common_add, result_list=result_list, store=store)
    for k in mq_quarter_indicator_enum.cal_avg_list:
        name = k.name
        i1 = call_find_now(period=period, name=name)
        i2 = call_find_pre(period=period_delta(period, -1), name=name)
        i3 = call_find_pre(period=period_delta(period, -2), name=name)
        i4 = call_find_pre(period=period_delta(period, -3), name=name)
        avg = mq_quarter_indicator.cal_ltm_avg(i1, i2, i3, i4)
        if avg is None:
            common_log_err(ts_code, period, update_date, '%s_ltm_avg' % name)
        else:
            call_add(to_add=avg)


def common_dividend(call_add: partial, call_log: partial, i1: MqQuarterIndicator, i2: MqQuarterIndicator, name: str):
    i = mq_quarter_indicator.dividend(i1, i2, name)
    if i is None:
        call_log(name=name)
    else:
        call_add(to_add=i)


def cal_du_pont(result_list: list, store: MqQuarterStore, period: str, ts_code: str, update_date: str):
    call_find = partial(store.find_period_exact, ts_code=ts_code, period=period, update_date=update_date)
    call_add = partial(common_add, result_list=result_list, store=store)
    call_log = partial(common_log_err, ts_code=ts_code, period=period, update_date=update_date)
    dprofit_ltm = call_find(name='dprofit_ltm')
    revenue_ltm = call_find(name='revenue_ltm')
    nasset_ltm_avg = call_find(name='nassets_ltm_avg')
    total_assets_ltm_avg = call_find(name='total_assets_ltm_avg')

    common_dividend(call_add, call_log, dprofit_ltm, nasset_ltm_avg, 'roe')
    common_dividend(call_add, call_log, dprofit_ltm, revenue_ltm, 'dprofit_margin')
    common_dividend(call_add, call_log, revenue_ltm, total_assets_ltm_avg, 'turnover_rate')
    common_dividend(call_add, call_log, total_assets_ltm_avg, nasset_ltm_avg, 'equity_multiplier')


def cal_risk(result_list: list, store: MqQuarterStore, period: str, ts_code: str, update_date: str):
    call_find = partial(store.find_period_exact, ts_code=ts_code, period=period, update_date=update_date)
    call_add = partial(common_add, result_list=result_list, store=store)
    call_log = partial(common_log_err, ts_code=ts_code, period=period, update_date=update_date)
    notes_receiv = call_find(name='notes_receiv')
    accounts_receiv = call_find(name='accounts_receiv')
    oth_receiv = call_find(name='oth_receiv')
    lt_rec = call_find(name='lt_rec')
    total_receive = mq_quarter_indicator.add_up('total_receive', [notes_receiv, accounts_receiv, oth_receiv, lt_rec])
    revenue = call_find(name='revenue_ltm')
    common_dividend(call_add, call_log, total_receive, revenue, 'receive_risk')

    total_cur_liab = call_find(name='total_cur_liab')
    total_cur_assets = call_find(name='total_cur_assets')
    common_dividend(call_add, call_log, total_cur_liab, total_cur_assets, 'liquidity_risk')

    goodwill = call_find(name='goodwill')
    r_and_d = call_find(name='r_and_d')
    intan_assets = call_find(name='intan_assets')
    total_intangible = mq_quarter_indicator.add_up('total_intangible', [goodwill, r_and_d, intan_assets])
    nassets = call_find(name='nassets')
    oth_eqt_tools_p_shr = call_find(name='oth_eqt_tools_p_shr')
    nassets1 = mq_quarter_indicator.sub_from(nassets, [oth_eqt_tools_p_shr])
    common_dividend(call_add, call_log, total_intangible, nassets1, 'intangible_risk')

    money_cap = call_find(name='money_cap')
    oth_cur_assets = call_find(name='oth_cur_assets')
    lt_borr = call_find(name='lt_borr')
    st_borr = call_find(name='st_borr')
    cur = mq_quarter_indicator.add_up('cur', [money_cap, oth_cur_assets])
    borr = mq_quarter_indicator.add_up('borr', [lt_borr, st_borr])
    common_dividend(call_add, call_log, cur, borr, 'cash_debt_rate')

    nprofit_ltm = call_find(name=mq_quarter_indicator_enum.nprofit_ltm.name)
    dividend_ltm = call_find(name=mq_quarter_indicator_enum.dividend_ltm.name)
    common_dividend(call_add, call_log, dividend_ltm, nprofit_ltm, mq_quarter_indicator_enum.dividend_ratio.name)


def cal_indicator(result_list: list, store: MqQuarterStore, period: str, ts_code: str, update_date: str):
    cal_ltm(result_list, store, period, ts_code, update_date)
    cal_avg(result_list, store, period, ts_code, update_date)
    cal_du_pont(result_list, store, period, ts_code, update_date)
    cal_risk(result_list, store, period, ts_code, update_date)


def cal_complex(result_list: list, store: MqQuarterStore, period_set: set, ts_code: str, update_date: str):
    period_list = list(period_set)
    period_list.sort()
    for period in period_list:
        cal_indicator(result_list, store, period, ts_code, update_date)


def cal_inc_rate(n: MqQuarterIndicator, l: MqQuarterIndicator):
    if n is None or l is None:
        return None
    else:
        if mq_quarter_indicator_enum.is_percent_indicator(n.name):
            return decimal_utils.sub(n.value, l.value)
        else:
            return decimal_utils.yoy(n.value, l.value)


def cal_yoy_mom(result_list: list, store: MqQuarterStore):
    for i in result_list:  # type: MqQuarterIndicator
        lm = store.find_period_latest(i.ts_code, i.name, period_delta(i.period, -1))
        i.mom = cal_inc_rate(i, lm)
        ly = store.find_period_latest(i.ts_code, i.name, period_delta(i.period, -4))
        i.yoy = cal_inc_rate(i, ly)


def calculate(ts_code: str, share_name: str, from_date: str = None, to_date: str = get_current_dt()):
    session: Session = db_client.get_session()
    if from_date is None:
        latest: list = session.query(MqQuarterIndicator).filter(MqQuarterIndicator.ts_code == ts_code) \
            .order_by(MqQuarterIndicator.update_date.desc()).limit(1).all()
        if len(latest) > 0:
            from_date = format_delta(latest[0].update_date, 1)
        else:
            from_date = mq_calculate_start_date
    store = init_quarter_store(ts_code, format_delta(from_date, -1000))

    income_arr, adjust_income_arr, balance_arr, adjust_balance_arr, cash_arr, adjust_cash_arr, \
    fina_arr, dividend_arr, forecast_arr = ready_data(ts_code, from_date)

    result_list = []
    while from_date <= to_date:
        period_set = set([])
        #  TODO 调整修正

        while fit_update_date(from_date, adjust_income_arr, 'mq_ann_date'):
            extract_from_income(result_list, store, period_set, adjust_income_arr.pop(0))
        while fit_update_date(from_date, adjust_balance_arr, 'mq_ann_date'):
            extract_from_balance(result_list, store, period_set, adjust_balance_arr.pop(0))
        while fit_update_date(from_date, adjust_cash_arr, 'mq_ann_date'):
            extract_from_cash_flow(result_list, store, period_set, adjust_cash_arr.pop(0))
        while fit_update_date(from_date, dividend_arr, 'imp_ann_date'):
            extract_from_dividend(result_list, store, period_set, adjust_cash_arr.pop(0))
        # TODO 财报修正

        while fit_update_date(from_date, income_arr, 'mq_ann_date'):
            extract_from_income(result_list, store, period_set, income_arr.pop(0))
        while fit_update_date(from_date, balance_arr, 'mq_ann_date'):
            extract_from_balance(result_list, store, period_set, balance_arr.pop(0))
        while fit_update_date(from_date, cash_arr, 'mq_ann_date'):
            extract_from_cash_flow(result_list, store, period_set, cash_arr.pop(0))
        while fit_update_date(from_date, fina_arr, 'ann_date'):
            extract_from_fina_indicator(result_list, store, period_set, fina_arr.pop(0))
        # TODO 预测修正

        while fit_update_date(from_date, forecast_arr, 'ann_date'):
            extract_from_forecast(result_list, store, period_set, forecast_arr.pop(0))
        # TODO 人工预测

        if len(period_set) > 0:
            copy_from_latest(result_list, store, period_set, ts_code, from_date)
            fill_empty(result_list, store, period_set, ts_code, from_date)
            cal_complex(result_list, store, period_set, ts_code, from_date)

        from_date = format_delta(from_date, 1)

    cal_yoy_mom(result_list, store)
    return result_list


def calculate_and_insert(ts_code: str, share_name: str):
    result_list = calculate(ts_code, share_name)
    if len(result_list) > 0:
        session: Session = db_client.get_session()
        start = time.time()
        for item in result_list:  # type: MqQuarterBasic
            session.add(item)
        session.flush()
        session.close()
        log.info("Insert mq_quarter_indicator for %s: %s seconds" % (ts_code, time.time() - start))
    else:
        log.info('Nothing to insert into mq_quarter_indicator %s' % ts_code)


def calculate_by_code(ts_code: str):
    session: Session = db_client.get_session()
    stock: MqStockMark = session.query(MqStockMark).filter(MqStockMark.ts_code == ts_code).one()
    session.close()
    calculate_and_insert(ts_code, stock.share_name)


def recalculate_by_code(ts_code: str):
    session: Session = db_client.get_session()
    session.query(MqQuarterIndicator).filter(MqQuarterIndicator.ts_code == ts_code).delete()
    session.close()
    calculate_by_code(ts_code)


if __name__ == '__main__':
    calculate_by_code(sys.argv[1])
