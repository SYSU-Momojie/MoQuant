class MqQuarterIndicatorEnum(object):

    def __init__(self, name, explain, is_percent=False, from_name=None):
        self.name = name
        self.from_name = name if from_name is None else from_name
        self.explain = explain
        self.is_percent = is_percent


# income
revenue = MqQuarterIndicatorEnum('revenue', '营业收入')
nprofit = MqQuarterIndicatorEnum('nprofit', '归母净利润', from_name='n_income_attr_p')
total_nprofit = MqQuarterIndicatorEnum('total_nprofit', '净利润', from_name='n_income')

extract_from_income_list = [revenue, nprofit, total_nprofit]

# balance sheet
total_share = MqQuarterIndicatorEnum('total_share', '总股本')
notes_receiv = MqQuarterIndicatorEnum('notes_receiv', '应收票据')
accounts_receiv = MqQuarterIndicatorEnum('accounts_receiv', '应收账款')
oth_receiv = MqQuarterIndicatorEnum('oth_receiv', '其他应收款')
lt_rec = MqQuarterIndicatorEnum('lt_rec', '长期应收款')
total_cur_liab = MqQuarterIndicatorEnum('total_cur_liab', '流动负债合计')
total_cur_assets = MqQuarterIndicatorEnum('total_cur_assets', '流动资产合计')
goodwill = MqQuarterIndicatorEnum('goodwill', '商誉')
r_and_d = MqQuarterIndicatorEnum('r_and_d', '研发支出')
intan_assets = MqQuarterIndicatorEnum('intan_assets', '无形资产')
nassets = MqQuarterIndicatorEnum('nassets', '净资产', from_name='total_hldr_eqy_exc_min_int')
total_assets = MqQuarterIndicatorEnum('total_assets', '总资产')
oth_eqt_tools_p_shr = MqQuarterIndicatorEnum('oth_eqt_tools_p_shr', '优先股/永续债')
money_cap = MqQuarterIndicatorEnum('money_cap', '货币资金')
oth_cur_assets = MqQuarterIndicatorEnum('oth_cur_assets', '其他流动资产')
lt_borr = MqQuarterIndicatorEnum('lt_borr', '长期借款')
st_borr = MqQuarterIndicatorEnum('st_borr', '短期借款')

extract_from_bs_list = [total_share, notes_receiv, accounts_receiv, oth_receiv, lt_rec, total_cur_liab,
                        total_cur_assets, goodwill, r_and_d, intan_assets, nassets, total_assets, oth_eqt_tools_p_shr,
                        money_cap, oth_cur_assets, lt_borr, st_borr]

# cash flow
n_cashflow_act = MqQuarterIndicatorEnum('n_cashflow_act', '经营活动产生的现金流量净额')

extract_from_cf_list = [n_cashflow_act]

# fina indicator
dprofit = MqQuarterIndicatorEnum('dprofit', '归母扣非净利润', from_name='profit_dedt')

extract_from_fi_list = [dprofit]

# express
express_nprofit = MqQuarterIndicatorEnum('dprofit', '归母扣非净利润', from_name='n_income')
extract_from_express_list = [revenue, express_nprofit, total_assets, nassets]

# forecast
extract_from_forecast_list = [nprofit]

# dividend
dividend = MqQuarterIndicatorEnum('dividend', '分红总额')
dividend_ratio = MqQuarterIndicatorEnum('dividend_ratio', '分红率', is_percent=True)
dividend_ltm = MqQuarterIndicatorEnum('dividend_ltm', '分红LTM', from_name='dividend')


# ltm
revenue_quarter = MqQuarterIndicatorEnum('revenue_quarter', '营业收入-单季', from_name='revenue')
revenue_ltm = MqQuarterIndicatorEnum('revenue_ltm', '营业收入-LTM', from_name='revenue_quarter')
nprofit_quarter = MqQuarterIndicatorEnum('nprofit_quarter', '归母净利润-单季', from_name='nprofit')
nprofit_ltm = MqQuarterIndicatorEnum('nprofit_ltm', '归母净利润-LTM', from_name='nprofit_quarter')
dprofit_quarter = MqQuarterIndicatorEnum('dprofit_quarter', '归母扣非净利润-单季', from_name='dprofit')
dprofit_ltm = MqQuarterIndicatorEnum('dprofit_ltm', '归母扣非净利润-LTM', from_name='dprofit_quarter')

cal_quarter_list = [revenue_quarter, nprofit_quarter, dprofit_quarter]
cal_ltm_list = [revenue_ltm, nprofit_ltm, dprofit_ltm, dividend_ltm]

# avg
nassets_ltm_avg = MqQuarterIndicatorEnum('nassets_ltm_avg', '净资产-LTM平均')
total_assets_ltm_avg = MqQuarterIndicatorEnum('total_assets_ltm_avg', '总资产-LTM平均')
cal_avg_list = [nassets, total_assets]

# du pont
roe = MqQuarterIndicatorEnum('roe', '净资产收益率')
dprofit_margin = MqQuarterIndicatorEnum('dprofit_margin', '净利率', is_percent=True)
turnover_rate = MqQuarterIndicatorEnum('turnover_rate', '周转率', is_percent=True)
equity_multiplier = MqQuarterIndicatorEnum('equity_multiplier', '权益乘数', is_percent=True)

# risk
receive_risk = MqQuarterIndicatorEnum('receive_risk', '应收风险', is_percent=True)
liquidity_risk = MqQuarterIndicatorEnum('liquidity_risk', '流动性风险', is_percent=True)
intangible_risk = MqQuarterIndicatorEnum('intangible_risk', '无形风险', is_percent=True)
cash_debt_rate = MqQuarterIndicatorEnum('cash_debt_rate', '存贷比', is_percent=True)

risk_point = MqQuarterIndicatorEnum('risk_point', '存贷比', is_percent=True)

# fill
fill_dividend = MqQuarterIndicatorEnum('dividend', '分红总额', from_name='')
fill_dprofit = MqQuarterIndicatorEnum('dprofit', '分红总额', from_name='nprofit')
fill_after_copy_fail_list = [fill_dividend, fill_dprofit]

all_indicators_list = [
    # income
    revenue, nprofit, total_nprofit,
    # balance sheet
    total_share, notes_receiv, accounts_receiv, oth_receiv, lt_rec, total_cur_liab,
    total_cur_assets, goodwill, r_and_d, intan_assets, nassets, total_assets, oth_eqt_tools_p_shr,
    money_cap, oth_cur_assets, lt_borr, st_borr,
    # cash flow
    n_cashflow_act,
    # fina
    dprofit,
    # dividend
    dividend, dividend_ratio,
    # quarter
    revenue_quarter, nprofit_quarter, dprofit_quarter,
    # ltm
    revenue_ltm, nprofit_ltm, dprofit_ltm, dividend_ltm,
    # avg
    nassets_ltm_avg, total_assets_ltm_avg,
    # du pont
    roe, dprofit_margin, turnover_rate, equity_multiplier,
    # risk
    receive_risk, liquidity_risk, intangible_risk, cash_debt_rate,
    risk_point
]

all_indicators_map = {}
for i in all_indicators_list:  # type: MqQuarterIndicatorEnum
    all_indicators_map[i.name] = i


def is_percent_indicator(name: str) -> bool:
    i = all_indicators_map[name]
    return i is not None and i.is_percent