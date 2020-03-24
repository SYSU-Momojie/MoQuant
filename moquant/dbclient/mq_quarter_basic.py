"""
计算逻辑备忘
1. 对于调整：年中财报有对去年进行调整的，计算ltm时在去年Q4上加上调整值
"""
from sqlalchemy import Column, String, DECIMAL, Boolean, Index, INT

from moquant.dbclient.base import Base


class MqQuarterBasic(Base):
    __tablename__ = 'mq_quarter_basic'
    __table_args__ = (
        Index('code', 'ts_code'),
        Index('update', 'update_date'),
        Index('report', 'report_period'),
        Index('forecast', 'forecast_period'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    )

    ts_code = Column('ts_code', String(10), primary_key=True, comment='TS股票代码')
    share_name = Column('share_name', String(20), comment='股票名称')
    update_date = Column('update_date', String(10), primary_key=True, comment='更新日期，财报、预报、快报、调整、分红发布日期')
    report_period = Column('report_period', String(10), primary_key=True, comment='最近一个已披露财报报告期 yyyyMMdd')
    adjust_ly = Column('adjust_ly', Boolean, server_default='0', comment='调整往年')
    forecast_period = Column('forecast_period', String(10), primary_key=True, comment='最近一个已披露预报、快报报告期 yyyyMMdd')
    forecast_type = Column('forecast_type', INT, comment='类型 1-预报 2-快报')
    revenue_period = Column('revenue_period', String(10), comment='营业收入所属报告期 yyyyMMdd')
    revenue = Column('revenue', DECIMAL(30, 10), comment='累计营业收入')
    revenue_ly = Column('revenue_ly', DECIMAL(30, 10), comment='去年累计营业收入')
    revenue_yoy = Column('revenue_yoy', DECIMAL(30, 10), comment='累计营业收入增速-同比')
    quarter_revenue = Column('quarter_revenue', DECIMAL(30, 10), comment='单季营业收入')
    quarter_revenue_ly = Column('quarter_revenue_ly', DECIMAL(30, 10), comment='去年同季营业收入')
    quarter_revenue_yoy = Column('quarter_revenue_yoy', DECIMAL(30, 10), comment='单季营业收入增速-同比')
    revenue_ltm = Column('revenue_ltm', DECIMAL(30, 10), comment='营业收入-LTM')
    nprofit_period = Column('nprofit_period', String(10), comment='归母净利润所属报告期 yyyyMMdd')
    nprofit = Column('nprofit', DECIMAL(30, 10), comment='累计归母净利润')
    nprofit_ly = Column('nprofit_ly', DECIMAL(30, 10), comment='去年累计归母净利润')
    nprofit_yoy = Column('nprofit_yoy', DECIMAL(30, 10), comment='累计归母净利润增速-同比')
    quarter_nprofit = Column('quarter_nprofit', DECIMAL(30, 10), comment='单季归母净利润')
    quarter_nprofit_ly = Column('quarter_nprofit_ly', DECIMAL(30, 10), comment='去年同季归母净利润')
    quarter_nprofit_yoy = Column('quarter_nprofit_yoy', DECIMAL(30, 10), comment='单季归母净利润增速-同比')
    nprofit_ltm = Column('nprofit_ltm', DECIMAL(30, 10), comment='LTM归母净利润')
    dprofit_period = Column('dprofit_period', String(10), comment='归母扣非净利润所属报告期 yyyyMMdd')
    dprofit = Column('dprofit', DECIMAL(30, 10), comment='累计归母扣非净利润')
    dprofit_ly = Column('dprofit_ly', DECIMAL(30, 10), comment='去年累计归母扣非净利润')
    dprofit_yoy = Column('dprofit_yoy', DECIMAL(30, 10), comment='累计归母扣非净利润增速-同比')
    quarter_dprofit = Column('quarter_dprofit', DECIMAL(30, 10), comment='单季归母扣非净利润')
    quarter_dprofit_ly = Column('quarter_dprofit_ly', DECIMAL(30, 10), comment='去年同季归母扣非净利润')
    quarter_dprofit_yoy = Column('quarter_dprofit_yoy', DECIMAL(30, 10), comment='单季归母扣非净利润增速-同比')
    dprofit_ltm = Column('dprofit_ltm', DECIMAL(30, 10), comment='LTM归母扣非净利润')
    dprofit_forecast_one_time = Column('dprofit_forecast_one_time', Boolean, server_default='0', comment='预报扣非净利为一次性')
    eps = Column('eps', DECIMAL(30, 10), comment='每股收益')
    nassets = Column('nassets', DECIMAL(30, 10), comment='归母净资产')
    dividend = Column('dividend', DECIMAL(30, 10), comment='当期分红总额')
    dividend_ltm = Column('dividend_ltm', DECIMAL(30, 10), comment='LTM分红总额')
    dividend_ltm_yoy = Column('dividend_ltm_yoy', DECIMAL(30, 10), comment='LTM分红总额增速-同比')
    dividend_profit_ratio = Column('dividend_profit_ratio', DECIMAL(30, 10), comment='分红率')
    receive_risk = Column('receive_risk', DECIMAL(30, 10), comment='应收风险=(应收账款/票据+其它/长期应收)/营收')
    liquidity_risk = Column('liquidity_risk', DECIMAL(30, 10), comment='流动性风险=流动负债/流动资产')
    intangible_risk = Column('intangible_risk', DECIMAL(30, 10), comment='无形风险=(商誉+开发支出+无形资产)/(净资产-优先股-永续债)')
    roe = Column('roe', DECIMAL(30, 10), comment='净资产收益率=LTM扣非净利/平均净资产')
    dprofit_margin = Column('dprofit_margin', DECIMAL(30, 10), comment='净利率=LTM扣非净利/LTM营收')
    turnover_rate = Column('turnover_rate', DECIMAL(30, 10), comment='周转率=LTM营收/平均总资产')
    equity_multiplier = Column('equity_multiplier', DECIMAL(30, 10), comment='权益乘数=平均总资产/平均净资产')
    cash_debt_rate = Column('cash_debt_rate', DECIMAL(30, 10), comment='存贷比=(货币资金+其他流动资产)/(短期借款+长期借款)')
    nprofit_to_cf = Column('nprofit_to_cf', DECIMAL(30, 10), comment='利润现金流比=净利润/经营活动现金流')