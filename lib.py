# -*- coding: utf-8 -*-
#coding=gbk
import pickle
import re
import os
import datetime
import time
import pandas as pd
import tushare as ts
from urllib.request import urlopen
from urllib.request import Request
from define import *

def read_data(fn):
    data = []
    try:
        with open(fn, 'rb') as f:
            data = pickle.load(f)
        f.close()
        return(data)
    except Exception as e:
        if( re.search('No such file or directory:', str(e)) != None ):
            print("No file to read.")
        else:
            print(str(e))
        return(data)
def save_data(fn, data):
    with open(fn, 'wb') as f:
        pickle.dump(data, f)
    f.close()              
def share_exist(share_bank, ID):
    exist_flag = False
    if( len(share_bank) != 0 ):
        for i in range(len(share_bank)):
            if( share_bank[i].id == ID):
                exist_flag = True
                break
    return(exist_flag)
def share_add(share_bank, share):
    append_flag = False
    if( share_exist(share_bank, share.id) == False ):
        share_bank.append(share)
        append_flag = True
    return(append_flag)
def share_del(share_bank, ID):
    del_flag = False
    if( len(share_bank) != 0 ):
        for i in range(len(share_bank)):
            if( share_bank[i].id == ID):
                del share_bank[i]
                del_flag = True
                break
    return(del_flag)
def get_sina_id(sID):
    stkID = ''
    if( sID[0:2] == '00' ):
        stkID = 'sz'+sID
    elif( sID[0:2] == '30' ):
        stkID = 'sz'+sID
    elif( sID[0:2] == '60' ):
        stkID = 'sh'+sID
    else:
        print('in get_sina_name the id :', sID)
    return(stkID)  
def get_t_s_id(sID):
    stkID = ''
    if( sID[0:2] == '00' ):
        stkID = sID+'.SZ'
    elif( sID[0:2] == '30' ):
        stkID = sID+'.SZ'
    elif( sID[0:2] == '60' ):
        stkID = sID+'.SH'
    else:
        print('in get_t_s_name the id :', sID)
    return(stkID)  
def is_pseudo_number(num):
    isflag = False
    if( num == None ):
        isflag = True
    elif( num == 'None' ):
        isflag = True
    else:
        if( num != num ):
            isflag = True
    return(isflag)
def get_name_price(s_code):                   # get name and current price
    url = url_quotation_before + get_sina_id(s_code)
    req = Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36') 
    try_done = False
    while try_done == False :
        try_done = True
        try:
            quots = urlopen(req).read()
        except Exception as e:
            print('---2--- : ' + str(e))
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            try_done = False
            time.sleep(300)
    quot = quots.decode('gbk')
    quot_msg = quot.split(',')
    if( len(quot_msg) > 3 ):
        name = quot_msg[0].split(u'="')[1]
        price = float(quot_msg[3])
    else:
        name = ''
        price = 0.0
    return(name, price)
def get_today():
    today=datetime.date.today()
    formatted_today=today.strftime('%Y%m%d')
    return( formatted_today )
def get_last_x_years(x):
    years = []
    for i in range(x):
        years.append(str(int(get_today()[0:4]) - 1 - i) + '1231')
    return(years)
def req_tushare(pro, mode, para):
    if( mode == 'query'):
        try:
            df = pro.query('fina_indicator', ts_code=para[0], period=para[1])
        except Exception as e:
            print(str(e))
            os._exit(0)
    else:
        df = None
        print('mode:', mode, ' not exist.')
    return(df)
def dividend_one_year(df, year):
    dqexe = []
    dqplan = []
    #获得实施记录
    for dfr in df.iterrows():
        dt = dfr[1]
        if(dt['end_date'][0:4] == year):
            if(dt['div_proc'].find(u'实施') != -1):
                dqexe.append([dt['end_date'], dt['div_proc'],dt['cash_div_tax'], dt['record_date']])
    #获得预案记录
    for dfr in df.iterrows():
        dt = dfr[1]
        if(dt['end_date'][0:4] == year):
            if(dt['div_proc'].find(u'预案') != -1):
                dqplan.append([dt['end_date'], dt['div_proc'],dt['cash_div_tax'], dt['record_date']])
    #获得真正的分配红利
    if( len(dqplan) != 0 ):
        for i in range(len(dqplan)-1, -1, -1):
            if( len(dqexe) != 0 ):
                for j in range(len(dqexe)):
                    if(dqplan[i][0] == dqexe[j][0]):
                        del dqplan[i]
                        break
                        if( i == 0 ):
                            break
    #累计红利 
    Dvdd = 0
    if( len(dqplan) != 0 ):           
        Dvdd += dqplan[0][2]
    if( len(dqexe) != 0 ):           
        for i in range(len(dqexe)):
            Dvdd += dqexe[i][2]
    return(Dvdd)
def dividends_for_stock(code, pro, today):                   # get last 6 years
    Ddd = []
    Ddd.append(str(int(today[0:4])-1)+'1231')
    dqdiv = []
    df = pro.dividend(ts_code=get_t_s_id(code), fields='cash_div_tax,div_proc,end_date,record_date,ex_date,stk_bo_rate,stk_co_rate,stk_div')
    for i in range(1, 6):
        year = str( int(today[0:4])-i )
        Ddd.append(round(dividend_one_year(df, year),4))
    for dfr in df.iterrows():
        dt = dfr[1]
        if(dt['end_date'][0:4] == str( int(today[0:4])-1 ) ):
            #最近转送股，调整股息率用
            if(dt['div_proc'].find(u'实施') != -1): 
                if( len(dqdiv) == 0 ):
                    dqdiv.append([dt['ex_date'], dt['stk_bo_rate'],dt['stk_co_rate'], dt['stk_div']])
                else:
                    print(u'---有转送!---')
    return(Ddd, dqdiv)
def get_last_qtr():
    this_year = int(get_today()[0:4])
    last_quarter = str(this_year-1) + Quarter[3]
    for i in range(4):
        iQtr = str(this_year) + Quarter[i]
        if( int(iQtr) <= int(get_today()) ):
            last_quarter = iQtr
        else:
            break
    return(last_quarter)
def get_last5qtrs():
    last5qtrs = []
    last5qtrs.append(get_last_qtr())
    for i in range(4):
        for j in range(4):
            if( last5qtrs[i][4:8] == Quarter[j]): 
                if( j == 0 ):
                    x = int(str(last5qtrs[i][0:4])) - 1
                    x = str(x) + Quarter[3]
                else:
                    x = int(str(last5qtrs[i][0:4]))
                    x = str(x) + Quarter[j-1]
                last5qtrs.append(x)    
    return(last5qtrs)
def eps_these_years(code, pro, year):              # 这些年的每股收益
    epss = []
    epss.append(year[0])
    for i in range(len(year)):
        df = pro.query('fina_indicator', ts_code=get_t_s_id(code), period=year[i])
        if(len(df) == 0):
            epss.append('None')
        else:
            for dfr in df.iterrows():
                dt = dfr[1]
                epss.append(dt['eps'])
    return(epss)
def eps_these_quarters(code, pro):            # 这些季度的每股收益
    last5qtrs = get_last5qtrs()
    EPSs = [last5qtrs[0]]   
    for i in range(len(last5qtrs)):
        df = pro.query('fina_indicator', ts_code=get_t_s_id(code), period=last5qtrs[i])
        if(len(df) == 0):
            EPSs.append(0.0)
        else:
            for dfr in df.iterrows():
                dt = dfr[1]
                if(not is_pseudo_number(dt['eps'])):
                    EPSs.append(dt['eps'])
                else:
                    EPSs.append(0.0)
    return(EPSs)
def fina_indicator(code, pro):           	  # 准备利润增速数据   每股经营活动产生的现金流量净额 和 流动比率
    last5qtrs = get_last5qtrs()
    # 准备利润增速数据
    pft=[]
    rt={}
    df = pro.query('fina_indicator', ts_code=get_t_s_id(code), start_date=last5qtrs[4], end_date=get_today())
    for dfr in df.iterrows():
        dt = dfr[1]
        if( len(pft) == 0 ):
            pft.append(dt['end_date'])
            # 每股经营活动产生的现金流量净额
            if( not is_pseudo_number(dt['ocfps']) ):
                rt['ocfps'] = dt['ocfps']
            # 基本每股收益
            if( not is_pseudo_number(dt['eps']) ):
                rt['eps'] = dt['eps']
            # 流动比率
            if( not is_pseudo_number(dt['current_ratio']) ):
                rt['current_ratio'] = dt['current_ratio']
            else:
                rt['current_ratio'] = None
        pft.append(dt['profit_dedt'])
    rt['pft'] = pft
    return(rt)
def calc_income_up(dividend):                   #  计算稳升
    up = 'Y'
    ud = 0.0
    for i in range(len(dividend)-1, 0, -1):
        if( dividend[i] >= ud ):
            ud = dividend[i]
        else:
            up = 'N'
    return(up)
def calc_pft_acc(pft):                     # 计算季报增速
    if( len(pft) > 5 ):
        return( round(pft[1]/pft[5]-1, 4) )
    else:
        return(-1)
def calc_gold_include(ocfps, eps):                    # 计算含金量
    if( eps != 0 ):
        gold_include = round( ocfps / eps, 3 )
    else:
        gold_include = -99.99
    return(round(gold_include, 3))
def calc_convert_rate(convert):            # 计算股份调整率
    rate = 1
    if( (not is_pseudo_number(convert[3])) and convert[3] != 0 ):
        rate += convert[3]
    return(rate)
def calc_avg_div_rates(div_rate):                   # 计算5年平均分红率 
    rt = 0
    yr = 5
    for i in range(1, 6):
        if( div_rate[i] <= 1 and div_rate[i] >= 0 ):
            rt += div_rate[i]
        else:
            yr -= 1
    if( yr != 0 ):
        return( round(rt/yr, 3) )
    else:
        return(0.0)
def calc_div_status(safe_div, avg_div_rate):                      # 是否保底分红率小于5年平均分红率    
    if( safe_div <= avg_div_rate ):
        div_status = 'Y'
    else:
        div_status = 'N'
    return(div_status)
def calc_stk_div_ratio(price, dividend, convert_rate):     # 当前股息率
    L1 = is_pseudo_number(convert_rate)
    L2 = is_pseudo_number(dividend[1])
    if( price != 0 ):
        if( (not L1) and (not L2) ):
            rt = round(dividend[1]/price/convert_rate, 3)
    else:
        rt = None
    return(rt)
def get_forecast(code, pro):
    s_date = get_last_qtr()[0:6] + '01'
    df = pro.forecast(ts_code=get_t_s_id(code), start_date=s_date, end_date=get_today(), fields='type, end_date, p_change_min, p_change_max, net_profit_min, net_profit_max')
    for dfr in df.iterrows():
        dt = dfr[1]
        print('--- start : ', s_date, ' ## ', end='')
        if( len(dt) != 0 ):
            print(dt)
        print('[]')
def get_express(code, pro):
    s_date = get_last_qtr()[0:6] + '01'
    df = pro.express(ts_code=get_t_s_id(code), start_date=s_date, end_date=get_today(), fields='ann_date, end_date, n_income, diluted_eps, yoy_tp, yoy_eps')
    for dfr in df.iterrows():
        dt = dfr[1]
        print('--- start: ', s_date, ' ## ', end='')
        if( len(dt) != 0 ):
            print(dt)
        print('[]')
def profit_dedt_last_five_years(code, years):
    profit_dedt = []
    profit_dedt.append(years[0])
    for i in range(len(years)):
        rd = RawData()
        df = rd.req_tushare_query(code, years[i])
        profit_dedt.append(df.iloc[0]['profit_dedt'])
    return(profit_dedt)        

class Share():
    df_stock_basic = None
    has_stock_basic = False
    today = get_today()
    ts.set_token(TOKEN)
    pro = ts.pro_api()
    def __init__(self):
        self.id = ''
        self.name =''
        self.price = 0.0
        self.flag = {}
        self.dt = {}          # 原始数据
        self.rt = {}          # 计算结果
        self.cp = {}          # 与price相关的计算结果
    @classmethod
    def stock_basic_df(cls):
        if( not cls.has_stock_basic ):
            cls.has_stock_basic = True
            cls.df_stock_basic = cls.pro.stock_basic(exchange='', list_status='L', fields='symbol,area,industry,list_date')
        return(cls.df_stock_basic)
    def nmcard(self):
        return(self.id+'['+self.name+']')
    def name_price_fill(self):
        self.name, self.price = get_name_price(self.id)
    def prt(self):
        print(self.nmcard())
    def stock_basic_fill(self):
        df = Share.stock_basic_df()
        for dfr in df.iterrows():
            dt = dfr[1]
            if( dt['symbol'] == self.id ):
                self.dt['industry'] = dt['industry']
                self.dt['area'] = dt['area']
                self.dt['list_date'] = dt['list_date']
        return()
    def last_five_years_dividend(self,cls):
        dividends_last, dq_div = dividends_for_stock(self.id, cls.pro, cls.today)
        self.dt['dividend'] = dividends_last
        for i in range(6):
            self.dt['convert'] = ['', 0.0, 0.0, 0.0]   # 转送股
            if( len(dq_div) != 0 ):
                for i in range(4):
                    if( not is_pseudo_number(dq_div[0][i]) ):
                        self.dt['convert'][i] = dq_div[0][i]
    def last_five_years_EPS(self,cls):
        year = get_last_x_years(5)
        epss = eps_these_years(self.id, cls.pro, year)
        self.dt['EPS'] = epss
    def calc_lfy_div_rate(self):         # 类内计算 --- 计算5年分红率
        dr = []
        if(self.dt['EPS'][0] == self.dt['dividend'][0]):
            dr.append(self.dt['EPS'][0])
            for i in range(1, 6):
                if( self.dt['dividend'][i] == 0.0 ):
                    div_rate = 0.0
                else:
                    if(not is_pseudo_number(self.dt['EPS'][i])):
                        div_rate = self.dt['dividend'][i] / self.dt['EPS'][i]
                    else:
                        div_rate = -1.0
                dr.append(round(div_rate, 4))
        else:
            print('--- wrong in func lfy_div_rate() ---')
        self.rt['div_rate'] = dr
    def last_five_quarters_EPS(self,cls):
        qs_eps = eps_these_quarters(self.id, cls.pro)
        self.dt['EPS_qtr'] = qs_eps
    def get_EPS_TTM(self):
        last_5_qtrs = []
        last_5_qtrs.append(get_last_qtr())
        x = get_last5qtrs()
        for i in range(5):
            last_5_qtrs.append(x[i])
        if( last_5_qtrs[1][4:8] == '1231' ):
            eps_ttm = self.dt['EPS_qtr'][1]
        else:
            eps_q = self.dt['EPS_qtr']
            for i in range(2,6):
                if( last_5_qtrs[i][4:8] == '1231'):
                    eps_ttm = eps_q[1] + eps_q[i] - eps_q[5]
                    break
        self.rt['EPS_ttm'] = round(eps_ttm, 3)
    def get_fina_data(self,cls):
        rt = fina_indicator(self.id,cls.pro)
        if( 'pft' in rt ):
            self.dt['profit_dedt'] = rt['pft']
        else:
            self.dt['profit_dedt'] = 0
        if( 'ocfps' in rt ):
            self.dt['ocfps'] = rt['ocfps']
        else:
            self.dt['ocfps'] = None
        if( 'eps' in rt ):
            self.dt['eps'] = rt['eps']
        else:
            self.dt['eps'] = 0.0
        if( 'current_ratio' in rt ):
            self.dt['current_ratio'] = rt['current_ratio']
        else:
            self.dt['current_ratio'] = 1
    def get_net_income(self,cls):           # 净利润 
        df = cls.pro.income(ts_code=get_t_s_id(self.id), start_date=get_last_qtr(), end_date=get_today(), fields='n_income')
        for dfr in df.iterrows():
            dt = dfr[1]
            if( not is_pseudo_number(dt['n_income']) ):
                self.dt['n_income'] = dt['n_income']
            else:
                self.dt['n_income'] = None
    def get_total_share(self,cls):              # 总股本
        df = cls.pro.balancesheet(ts_code=get_t_s_id(self.id), start_date=get_last_qtr(), end_date=get_today(), fields='total_share')
        for dfr in df.iterrows():
            dt = dfr[1]
            if( not is_pseudo_number(dt['total_share']) ):
                self.dt['total_share'] = dt['total_share']
            else:
                self.dt['total_share'] = None
    def get_base(self):
        self.name_price_fill()
        self.stock_basic_fill()
        self.last_five_years_dividend(self)
        self.last_five_years_EPS(self)
        self.last_five_quarters_EPS(self)
        self.get_EPS_TTM()
        self.get_fina_data(self)
        self.get_net_income(self)
        self.get_total_share(self)
    def calc(self):
        self.calc_lfy_div_rate()
        self.get_EPS_TTM()
        self.rt['income_up'] = calc_income_up(self.dt['dividend'])
        self.rt['profit_dedt_acc'] = calc_pft_acc(self.dt['profit_dedt'])                         # 净利润季报增速
        self.rt['gold_include'] = calc_gold_include(self.dt['ocfps'], self.dt['eps'])
        self.rt['convert_rate'] = calc_convert_rate(self.dt['convert'])
        self.rt['avg_div_rate'] = calc_avg_div_rates(self.rt['div_rate'])
        self.rt['last_year_div'] = round( self.dt['dividend'][1]/self.rt['convert_rate'], 3)           # 最新年度分红
    def calc_cp(self):
        self.cp['stk_div_ratio'] = calc_stk_div_ratio(self.price, self.dt['dividend'], self.rt['convert_rate'])   # 当前股息率
        self.cp['hope_div'] = round(self.price * hope_dividend_ratio, 3)          # 期望保底分红
        if( self.rt['EPS_ttm'] != 0 ):
            self.cp['safe_div'] = round( self.cp['hope_div']/self.rt['EPS_ttm'], 3)           # 保底分红率 = 期望保底分红 /EPS_TTM
        else:
            self.cp['safe_div'] = 9.99           # 保底分红率 = 期望保底分红 /EPS_TTM
        self.cp['div_status'] = calc_div_status(self.cp['safe_div'], self.rt['avg_div_rate'])
    def forecast(self,cls):
        get_forecast(self.id, cls.pro)
    def express(self,cls):
        get_forecast(self.id, cls.pro)
    def profit_dedt(self,cls):
        years = get_last_x_years(5)
        profit_dedt = profit_dedt_last_five_years(self.id, years)
        self.dt['profit_dedt_years'] = profit_dedt
        print(profit_dedt)
class RawData():
    ts.set_token(TOKEN)
    pro = ts.pro_api()
    df_query = pd.DataFrame()
    @classmethod
    def reset(cls):
        cls.df_query = pd.DataFrame()
    @classmethod    
    def req_tushare_query(cls, code, period):
        get = False
        if(cls.df_query.shape[0] != 0):
            for i in range(cls.df_query.shape[0]):
                if( cls.df_query.iloc[i]['end_date'] == period ):
                    df = cls.df_query.iloc[[i]]
                    print('-smart work-')
                    get = True
                    break
        if( get == False ):
            mode = 'query'
            para = []
            para.append(get_t_s_id(code))
            para.append(period)
            df = req_tushare(cls.pro, mode, para)
            cls.df_query = cls.df_query.append(df, ignore_index=True)
            print('req')
        return(df)
