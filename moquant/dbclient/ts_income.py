""" Declaration of table `ts_income` """

from sqlalchemy import Column, String, DECIMAL, BIGINT, Index

from moquant.dbclient.base import Base


class TsIncome(Base):
    __tablename__ = 'ts_income'
    __table_args__ = (
        Index('code_date', 'ts_code', 'mq_ann_date', 'end_date'),
        Index('code_period', 'ts_code', 'end_date'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    )

    id = Column('id', BIGINT, primary_key=True, comment='id', autoincrement=True)
    ts_code = Column('ts_code', String(10), comment='TS代码')
    ann_date = Column('ann_date', String(10), comment='公告日期')
    f_ann_date = Column('f_ann_date', String(10), comment='实际公告日期')
    mq_ann_date = Column('mq_ann_date', String(10), comment='MQ使用公告日期')
    end_date = Column('end_date', String(10), comment='报告期')
    report_type = Column('report_type', String(10), comment='报告类型 1合并报表, 4调整合并')
    comp_type = Column('comp_type', String(10), comment='公司类型(1一般工商业2银行3保险4证券)')
    basic_eps = Column('basic_eps', DECIMAL(30, 10), comment='基本每股收益')
    diluted_eps = Column('diluted_eps', DECIMAL(30, 10), comment='稀释每股收益')
    total_revenue = Column('total_revenue', DECIMAL(30, 10), comment='营业总收入')
    revenue = Column('revenue', DECIMAL(30, 10), comment='营业收入')
    int_income = Column('int_income', DECIMAL(30, 10), comment='利息收入')
    prem_earned = Column('prem_earned', DECIMAL(30, 10), comment='已赚保费')
    comm_income = Column('comm_income', DECIMAL(30, 10), comment='手续费及佣金收入')
    n_commis_income = Column('n_commis_income', DECIMAL(30, 10), comment='手续费及佣金净收入')
    n_oth_income = Column('n_oth_income', DECIMAL(30, 10), comment='其他经营净收益')
    n_oth_b_income = Column('n_oth_b_income', DECIMAL(30, 10), comment='加:其他业务净收益')
    prem_income = Column('prem_income', DECIMAL(30, 10), comment='保险业务收入')
    out_prem = Column('out_prem', DECIMAL(30, 10), comment='减:分出保费')
    une_prem_reser = Column('une_prem_reser', DECIMAL(30, 10), comment='提取未到期责任准备金')
    reins_income = Column('reins_income', DECIMAL(30, 10), comment='其中:分保费收入')
    n_sec_tb_income = Column('n_sec_tb_income', DECIMAL(30, 10), comment='代理买卖证券业务净收入')
    n_sec_uw_income = Column('n_sec_uw_income', DECIMAL(30, 10), comment='证券承销业务净收入')
    n_asset_mg_income = Column('n_asset_mg_income', DECIMAL(30, 10), comment='受托客户资产管理业务净收入')
    oth_b_income = Column('oth_b_income', DECIMAL(30, 10), comment='其他业务收入')
    fv_value_chg_gain = Column('fv_value_chg_gain', DECIMAL(30, 10), comment='加:公允价值变动净收益')
    invest_income = Column('invest_income', DECIMAL(30, 10), comment='加:投资净收益')
    ass_invest_income = Column('ass_invest_income', DECIMAL(30, 10), comment='其中:对联营企业和合营企业的投资收益')
    forex_gain = Column('forex_gain', DECIMAL(30, 10), comment='加:汇兑净收益')
    total_cogs = Column('total_cogs', DECIMAL(30, 10), comment='营业总成本')
    oper_cost = Column('oper_cost', DECIMAL(30, 10), comment='减:营业成本')
    int_exp = Column('int_exp', DECIMAL(30, 10), comment='减:利息支出')
    comm_exp = Column('comm_exp', DECIMAL(30, 10), comment='减:手续费及佣金支出')
    biz_tax_surchg = Column('biz_tax_surchg', DECIMAL(30, 10), comment='减:营业税金及附加')
    sell_exp = Column('sell_exp', DECIMAL(30, 10), comment='减:销售费用')
    admin_exp = Column('admin_exp', DECIMAL(30, 10), comment='减:管理费用')
    fin_exp = Column('fin_exp', DECIMAL(30, 10), comment='减:财务费用')
    assets_impair_loss = Column('assets_impair_loss', DECIMAL(30, 10), comment='减:资产减值损失')
    prem_refund = Column('prem_refund', DECIMAL(30, 10), comment='退保金')
    compens_payout = Column('compens_payout', DECIMAL(30, 10), comment='赔付总支出')
    reser_insur_liab = Column('reser_insur_liab', DECIMAL(30, 10), comment='提取保险责任准备金')
    div_payt = Column('div_payt', DECIMAL(30, 10), comment='保户红利支出')
    reins_exp = Column('reins_exp', DECIMAL(30, 10), comment='分保费用')
    oper_exp = Column('oper_exp', DECIMAL(30, 10), comment='营业支出')
    compens_payout_refu = Column('compens_payout_refu', DECIMAL(30, 10), comment='减:摊回赔付支出')
    insur_reser_refu = Column('insur_reser_refu', DECIMAL(30, 10), comment='减:摊回保险责任准备金')
    reins_cost_refund = Column('reins_cost_refund', DECIMAL(30, 10), comment='减:摊回分保费用')
    other_bus_cost = Column('other_bus_cost', DECIMAL(30, 10), comment='其他业务成本')
    operate_profit = Column('operate_profit', DECIMAL(30, 10), comment='营业利润')
    non_oper_income = Column('non_oper_income', DECIMAL(30, 10), comment='加:营业外收入')
    non_oper_exp = Column('non_oper_exp', DECIMAL(30, 10), comment='减:营业外支出')
    nca_disploss = Column('nca_disploss', DECIMAL(30, 10), comment='其中:减:非流动资产处置净损失')
    total_profit = Column('total_profit', DECIMAL(30, 10), comment='利润总额')
    income_tax = Column('income_tax', DECIMAL(30, 10), comment='所得税费用')
    n_income = Column('n_income', DECIMAL(30, 10), comment='净利润(含少数股东损益)')
    n_income_attr_p = Column('n_income_attr_p', DECIMAL(30, 10), comment='净利润(不含少数股东损益)')
    minority_gain = Column('minority_gain', DECIMAL(30, 10), comment='少数股东损益')
    oth_compr_income = Column('oth_compr_income', DECIMAL(30, 10), comment='其他综合收益')
    t_compr_income = Column('t_compr_income', DECIMAL(30, 10), comment='综合收益总额')
    compr_inc_attr_p = Column('compr_inc_attr_p', DECIMAL(30, 10), comment='归属于母公司(或股东)的综合收益总额')
    compr_inc_attr_m_s = Column('compr_inc_attr_m_s', DECIMAL(30, 10), comment='归属于少数股东的综合收益总额')
    ebit = Column('ebit', DECIMAL(30, 10), comment='息税前利润')
    ebitda = Column('ebitda', DECIMAL(30, 10), comment='息税折旧摊销前利润')
    insurance_exp = Column('insurance_exp', DECIMAL(30, 10), comment='保险业务支出')
    undist_profit = Column('undist_profit', DECIMAL(30, 10), comment='年初未分配利润')
    distable_profit = Column('distable_profit', DECIMAL(30, 10), comment='可分配利润')
    update_flag = Column('update_flag', String(10), comment='更新标识')


def create(engine):
    Base.metadata.create_all(engine)
