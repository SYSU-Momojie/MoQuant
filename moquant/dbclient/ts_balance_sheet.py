from sqlalchemy import Column, String, DECIMAL, BIGINT, Index

from moquant.dbclient.base import Base


class TsBalanceSheet(Base):
    __tablename__ = 'ts_balance_sheet'
    __table_args__ = (
        Index('code_date', 'ts_code', 'mq_ann_date', 'end_date'),
        Index('code_period', 'ts_code', 'end_date'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    )

    id = Column('id', BIGINT, primary_key=True, comment='id', autoincrement=True)
    ts_code = Column('ts_code', String(10), comment='TS股票代码')
    ann_date = Column('ann_date', String(10), comment='公告日期')
    f_ann_date = Column('f_ann_date', String(10), comment='实际公告日期')
    mq_ann_date = Column('mq_ann_date', String(10), comment='MQ使用公告日期')
    end_date = Column('end_date', String(10), comment='报告期')
    report_type = Column('report_type', String(10), comment='报表类型')
    comp_type = Column('comp_type', String(10), comment='公司类型')
    total_share = Column('total_share', DECIMAL(30, 10), comment='期末总股本')
    cap_rese = Column('cap_rese', DECIMAL(30, 10), comment='资本公积金')
    undistr_porfit = Column('undistr_porfit', DECIMAL(30, 10), comment='未分配利润')
    surplus_rese = Column('surplus_rese', DECIMAL(30, 10), comment='盈余公积金')
    special_rese = Column('special_rese', DECIMAL(30, 10), comment='专项储备')
    money_cap = Column('money_cap', DECIMAL(30, 10), comment='货币资金')
    trad_asset = Column('trad_asset', DECIMAL(30, 10), comment='交易性金融资产')
    notes_receiv = Column('notes_receiv', DECIMAL(30, 10), comment='应收票据', server_default=0)
    accounts_receiv = Column('accounts_receiv', DECIMAL(30, 10), comment='应收账款')
    oth_receiv = Column('oth_receiv', DECIMAL(30, 10), comment='其他应收款')
    prepayment = Column('prepayment', DECIMAL(30, 10), comment='预付款项')
    div_receiv = Column('div_receiv', DECIMAL(30, 10), comment='应收股利')
    int_receiv = Column('int_receiv', DECIMAL(30, 10), comment='应收利息')
    inventories = Column('inventories', DECIMAL(30, 10), comment='存货')
    amor_exp = Column('amor_exp', DECIMAL(30, 10), comment='长期待摊费用')
    nca_within_1y = Column('nca_within_1y', DECIMAL(30, 10), comment='一年内到期的非流动资产')
    sett_rsrv = Column('sett_rsrv', DECIMAL(30, 10), comment='结算备付金')
    loanto_oth_bank_fi = Column('loanto_oth_bank_fi', DECIMAL(30, 10), comment='拆出资金')
    premium_receiv = Column('premium_receiv', DECIMAL(30, 10), comment='应收保费')
    reinsur_receiv = Column('reinsur_receiv', DECIMAL(30, 10), comment='应收分保账款')
    reinsur_res_receiv = Column('reinsur_res_receiv', DECIMAL(30, 10), comment='应收分保合同准备金')
    pur_resale_fa = Column('pur_resale_fa', DECIMAL(30, 10), comment='买入返售金融资产')
    oth_cur_assets = Column('oth_cur_assets', DECIMAL(30, 10), comment='其他流动资产')
    total_cur_assets = Column('total_cur_assets', DECIMAL(30, 10), comment='流动资产合计')
    fa_avail_for_sale = Column('fa_avail_for_sale', DECIMAL(30, 10), comment='可供出售金融资产')
    htm_invest = Column('htm_invest', DECIMAL(30, 10), comment='持有至到期投资')
    lt_eqt_invest = Column('lt_eqt_invest', DECIMAL(30, 10), comment='长期股权投资')
    invest_real_estate = Column('invest_real_estate', DECIMAL(30, 10), comment='投资性房地产')
    time_deposits = Column('time_deposits', DECIMAL(30, 10), comment='定期存款')
    oth_assets = Column('oth_assets', DECIMAL(30, 10), comment='其他资产')
    lt_rec = Column('lt_rec', DECIMAL(30, 10), comment='长期应收款')
    fix_assets = Column('fix_assets', DECIMAL(30, 10), comment='固定资产')
    cip = Column('cip', DECIMAL(30, 10), comment='在建工程')
    const_materials = Column('const_materials', DECIMAL(30, 10), comment='工程物资')
    fixed_assets_disp = Column('fixed_assets_disp', DECIMAL(30, 10), comment='固定资产清理')
    produc_bio_assets = Column('produc_bio_assets', DECIMAL(30, 10), comment='生产性生物资产')
    oil_and_gas_assets = Column('oil_and_gas_assets', DECIMAL(30, 10), comment='油气资产')
    intan_assets = Column('intan_assets', DECIMAL(30, 10), comment='无形资产')
    r_and_d = Column('r_and_d', DECIMAL(30, 10), comment='研发支出')
    goodwill = Column('goodwill', DECIMAL(30, 10), comment='商誉')
    lt_amor_exp = Column('lt_amor_exp', DECIMAL(30, 10), comment='长期待摊费用')
    defer_tax_assets = Column('defer_tax_assets', DECIMAL(30, 10), comment='递延所得税资产')
    decr_in_disbur = Column('decr_in_disbur', DECIMAL(30, 10), comment='发放贷款及垫款')
    oth_nca = Column('oth_nca', DECIMAL(30, 10), comment='其他非流动资产')
    total_nca = Column('total_nca', DECIMAL(30, 10), comment='非流动资产合计')
    cash_reser_cb = Column('cash_reser_cb', DECIMAL(30, 10), comment='现金及存放中央银行款项')
    depos_in_oth_bfi = Column('depos_in_oth_bfi', DECIMAL(30, 10), comment='存放同业和其它金融机构款项')
    prec_metals = Column('prec_metals', DECIMAL(30, 10), comment='贵金属')
    deriv_assets = Column('deriv_assets', DECIMAL(30, 10), comment='衍生金融资产')
    rr_reins_une_prem = Column('rr_reins_une_prem', DECIMAL(30, 10), comment='应收分保未到期责任准备金')
    rr_reins_outstd_cla = Column('rr_reins_outstd_cla', DECIMAL(30, 10), comment='应收分保未决赔款准备金')
    rr_reins_lins_liab = Column('rr_reins_lins_liab', DECIMAL(30, 10), comment='应收分保寿险责任准备金')
    rr_reins_lthins_liab = Column('rr_reins_lthins_liab', DECIMAL(30, 10), comment='应收分保长期健康险责任准备金')
    refund_depos = Column('refund_depos', DECIMAL(30, 10), comment='存出保证金')
    ph_pledge_loans = Column('ph_pledge_loans', DECIMAL(30, 10), comment='保户质押贷款')
    refund_cap_depos = Column('refund_cap_depos', DECIMAL(30, 10), comment='存出资本保证金')
    indep_acct_assets = Column('indep_acct_assets', DECIMAL(30, 10), comment='独立账户资产')
    client_depos = Column('client_depos', DECIMAL(30, 10), comment='其中：客户资金存款')
    client_prov = Column('client_prov', DECIMAL(30, 10), comment='其中：客户备付金')
    transac_seat_fee = Column('transac_seat_fee', DECIMAL(30, 10), comment='其中:交易席位费')
    invest_as_receiv = Column('invest_as_receiv', DECIMAL(30, 10), comment='应收款项类投资')
    total_assets = Column('total_assets', DECIMAL(30, 10), comment='资产总计')
    lt_borr = Column('lt_borr', DECIMAL(30, 10), comment='长期借款')
    st_borr = Column('st_borr', DECIMAL(30, 10), comment='短期借款')
    cb_borr = Column('cb_borr', DECIMAL(30, 10), comment='向中央银行借款')
    depos_ib_deposits = Column('depos_ib_deposits', DECIMAL(30, 10), comment='吸收存款及同业存放')
    loan_oth_bank = Column('loan_oth_bank', DECIMAL(30, 10), comment='拆入资金')
    trading_fl = Column('trading_fl', DECIMAL(30, 10), comment='交易性金融负债')
    notes_payable = Column('notes_payable', DECIMAL(30, 10), comment='应付票据')
    acct_payable = Column('acct_payable', DECIMAL(30, 10), comment='应付账款')
    adv_receipts = Column('adv_receipts', DECIMAL(30, 10), comment='预收款项')
    sold_for_repur_fa = Column('sold_for_repur_fa', DECIMAL(30, 10), comment='卖出回购金融资产款')
    comm_payable = Column('comm_payable', DECIMAL(30, 10), comment='应付手续费及佣金')
    payroll_payable = Column('payroll_payable', DECIMAL(30, 10), comment='应付职工薪酬')
    taxes_payable = Column('taxes_payable', DECIMAL(30, 10), comment='应交税费')
    int_payable = Column('int_payable', DECIMAL(30, 10), comment='应付利息')
    div_payable = Column('div_payable', DECIMAL(30, 10), comment='应付股利')
    oth_payable = Column('oth_payable', DECIMAL(30, 10), comment='其他应付款')
    acc_exp = Column('acc_exp', DECIMAL(30, 10), comment='预提费用')
    deferred_inc = Column('deferred_inc', DECIMAL(30, 10), comment='递延收益')
    st_bonds_payable = Column('st_bonds_payable', DECIMAL(30, 10), comment='应付短期债券')
    payable_to_reinsurer = Column('payable_to_reinsurer', DECIMAL(30, 10), comment='应付分保账款')
    rsrv_insur_cont = Column('rsrv_insur_cont', DECIMAL(30, 10), comment='保险合同准备金')
    acting_trading_sec = Column('acting_trading_sec', DECIMAL(30, 10), comment='代理买卖证券款')
    acting_uw_sec = Column('acting_uw_sec', DECIMAL(30, 10), comment='代理承销证券款')
    non_cur_liab_due_1y = Column('non_cur_liab_due_1y', DECIMAL(30, 10), comment='一年内到期的非流动负债')
    oth_cur_liab = Column('oth_cur_liab', DECIMAL(30, 10), comment='其他流动负债')
    total_cur_liab = Column('total_cur_liab', DECIMAL(30, 10), comment='流动负债合计')
    bond_payable = Column('bond_payable', DECIMAL(30, 10), comment='应付债券')
    lt_payable = Column('lt_payable', DECIMAL(30, 10), comment='长期应付款')
    specific_payables = Column('specific_payables', DECIMAL(30, 10), comment='专项应付款')
    estimated_liab = Column('estimated_liab', DECIMAL(30, 10), comment='预计负债')
    defer_tax_liab = Column('defer_tax_liab', DECIMAL(30, 10), comment='递延所得税负债')
    defer_inc_non_cur_liab = Column('defer_inc_non_cur_liab', DECIMAL(30, 10), comment='递延收益-非流动负债')
    oth_ncl = Column('oth_ncl', DECIMAL(30, 10), comment='其他非流动负债')
    total_ncl = Column('total_ncl', DECIMAL(30, 10), comment='非流动负债合计')
    depos_oth_bfi = Column('depos_oth_bfi', DECIMAL(30, 10), comment='同业和其它金融机构存放款项')
    deriv_liab = Column('deriv_liab', DECIMAL(30, 10), comment='衍生金融负债')
    depos = Column('depos', DECIMAL(30, 10), comment='吸收存款')
    agency_bus_liab = Column('agency_bus_liab', DECIMAL(30, 10), comment='代理业务负债')
    oth_liab = Column('oth_liab', DECIMAL(30, 10), comment='其他负债')
    prem_receiv_adva = Column('prem_receiv_adva', DECIMAL(30, 10), comment='预收保费')
    depos_received = Column('depos_received', DECIMAL(30, 10), comment='存入保证金')
    ph_invest = Column('ph_invest', DECIMAL(30, 10), comment='保户储金及投资款')
    reser_une_prem = Column('reser_une_prem', DECIMAL(30, 10), comment='未到期责任准备金')
    reser_outstd_claims = Column('reser_outstd_claims', DECIMAL(30, 10), comment='未决赔款准备金')
    reser_lins_liab = Column('reser_lins_liab', DECIMAL(30, 10), comment='寿险责任准备金')
    reser_lthins_liab = Column('reser_lthins_liab', DECIMAL(30, 10), comment='长期健康险责任准备金')
    indept_acc_liab = Column('indept_acc_liab', DECIMAL(30, 10), comment='独立账户负债')
    pledge_borr = Column('pledge_borr', DECIMAL(30, 10), comment='其中:质押借款')
    indem_payable = Column('indem_payable', DECIMAL(30, 10), comment='应付赔付款')
    policy_div_payable = Column('policy_div_payable', DECIMAL(30, 10), comment='应付保单红利')
    total_liab = Column('total_liab', DECIMAL(30, 10), comment='负债合计')
    treasury_share = Column('treasury_share', DECIMAL(30, 10), comment='减:库存股')
    ordin_risk_reser = Column('ordin_risk_reser', DECIMAL(30, 10), comment='一般风险准备')
    forex_differ = Column('forex_differ', DECIMAL(30, 10), comment='外币报表折算差额')
    invest_loss_unconf = Column('invest_loss_unconf', DECIMAL(30, 10), comment='未确认的投资损失')
    minority_int = Column('minority_int', DECIMAL(30, 10), comment='少数股东权益')
    total_hldr_eqy_exc_min_int = Column('total_hldr_eqy_exc_min_int', DECIMAL(30, 10), comment='股东权益合计(不含少数股东权益)')
    total_hldr_eqy_inc_min_int = Column('total_hldr_eqy_inc_min_int', DECIMAL(30, 10), comment='股东权益合计(含少数股东权益)')
    total_liab_hldr_eqy = Column('total_liab_hldr_eqy', DECIMAL(30, 10), comment='负债及股东权益总计')
    lt_payroll_payable = Column('lt_payroll_payable', DECIMAL(30, 10), comment='长期应付职工薪酬')
    oth_comp_income = Column('oth_comp_income', DECIMAL(30, 10), comment='其他综合收益')
    oth_eqt_tools = Column('oth_eqt_tools', DECIMAL(30, 10), comment='其他权益工具')
    oth_eqt_tools_p_shr = Column('oth_eqt_tools_p_shr', DECIMAL(30, 10), comment='其他权益工具(优先股)')
    lending_funds = Column('lending_funds', DECIMAL(30, 10), comment='融出资金')
    acc_receivable = Column('acc_receivable', DECIMAL(30, 10), comment='应收款项')
    st_fin_payable = Column('st_fin_payable', DECIMAL(30, 10), comment='应付短期融资款')
    payables = Column('payables', DECIMAL(30, 10), comment='应付款项')
    hfs_assets = Column('hfs_assets', DECIMAL(30, 10), comment='持有待售的资产')
    hfs_sales = Column('hfs_sales', DECIMAL(30, 10), comment='持有待售的负债')
    update_flag = Column('update_flag', String(10), comment='更新标识')
