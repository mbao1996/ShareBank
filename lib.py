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

my_flag = 'goodu'
hd_flag = 'holding'
att_flag = 'attention'

def is_number(variate):
    flag = False
    if isinstance(variate,int):
        flag = True
    elif isinstance(variate,float):
        flag = True
    else:
        flag = False
    return(flag)
def is_list_number(list, start):
    if( start > len(list) ):
        return(False)
    for i in range(start, len(list)):
        if( not is_number(list[i]) ):
            return(False)
    return(True)
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
def has_flags(share_bank, flag):
    has = False
    for i in range(len(flag)):
        if( flag[i] in share_bank.flag ):
            if( share_bank.flag[flag[i]] == 'Y' ):
                has = True
    return(has)    
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
def other_day(the_day, diff):
    the_date = datetime.datetime.strptime(the_day, '%Y%m%d')
    other_day = the_date + datetime.timedelta(days=diff)
    return(other_day.strftime("%Y%m%d"))
def get_last_x_years(x):
    years = []
    for i in range(x):
        years.append(str(int(get_today()[0:4]) - 1 - i) + '1231')
    return(years)
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
def dividends_for_stock(rd, code, today):                   # get last 6 years
    Ddd = []
    Ddd.append(str(int(today[0:4])-1)+'1231')
    dqdiv = []
    df = rd.req_dividend(rd, code)
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
def last_qtr(data_from):
    last_year = int(data_from[0:4]) -1 
    last_quarter = str(last_year) + Quarter[3]
    for i in range(4):
        iQtr = data_from[0:4] + Quarter[i]
        if( int(iQtr) <= int(data_from) ):
            last_quarter = iQtr
    return(last_quarter)
def last_eight_qtrs(data_from):
    last8qtrs = []
    last8qtrs.append(last_qtr(data_from))
    for i in range(7):
        for j in range(4):
            if( last8qtrs[i][4:8] == Quarter[j]): 
                if( j == 0 ):
                    x = int(str(last8qtrs[i][0:4])) - 1
                    x = str(x) + Quarter[3]
                else:
                    x = int(str(last8qtrs[i][0:4]))
                    x = str(x) + Quarter[j-1]
                last8qtrs.append(x)    
    return(last8qtrs)
def eps_these_years(rd, code, year):              # 这些年的每股收益
    epss = []
    epss.append(year[0])
    for i in range(len(year)):
        df = rd.req_tushare_query(rd, code, year[i])
        if(len(df) == 0):
            epss.append('None')
        else:
            epss.append(df.iloc[0]['eps'])
    return(epss)        
def eps_these_quarters(rd, code):                  # 这些季度的每股收益
    last_qtrs = last_eight_qtrs(get_today())
    count = 0  
    for i in range(len(last_qtrs)):
        df = rd.req_tushare_query(rd, code, last_qtrs[i])
        if( len(df) != 0 ):
            if( count==0 ):
                EPSs = [last_qtrs[i]]
            if( is_number(df.iloc[0]['eps']) ):
                EPSs.append(df.iloc[0]['eps'])
            else:
                EPSs.append('None')
            count += 1
            if( count >= 5 ):
                break
    return(EPSs)
def fina_indicator(rd, code):           	  # 准备利润增速数据   每股经营活动产生的现金流量净额 和 流动比率
    last_qtrs = last_eight_qtrs(get_today())
    # 准备利润增速数据
    pft_qtr=[]
    rt={}
    count = 0
    for i in range(len(last_qtrs)):
        df = rd.req_tushare_query(rd, code, last_qtrs[i])
        if( len(df) != 0 ):
            if( count == 0 ):
                pft_qtr.append(df.iloc[0]['end_date'])
                # 每股经营活动产生的现金流量净额
                if( not is_pseudo_number(df.iloc[0]['ocfps']) ):
                    rt['ocfps'] = df.iloc[0]['ocfps']
                # 基本每股收益
                if( not is_pseudo_number(df.iloc[0]['eps']) ):
                    rt['eps'] = df.iloc[0]['eps']
                # 流动比率
                if( not is_pseudo_number(df.iloc[0]['current_ratio']) ):
                    rt['current_ratio'] = df.iloc[0]['current_ratio']
                else:
                    rt['current_ratio'] = None
            pft_qtr.append(df.iloc[0]['profit_dedt'])
            count += 1
            if( count >= 5 ):
                break
    rt['pft_qtr'] = pft_qtr
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
    if( len(pft) > 5 and pft[5] != None ):
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
def calc_div_status(safe_div, avg_div_rate):                     # 是否保底分红率小于5年平均分红率    
    if( is_number(safe_div) and is_number(avg_div_rate) ):
        if( safe_div <= avg_div_rate ):
            div_status = 'Y'
        else:
            div_status = 'N'
    else:
        div_status = ''
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
def get_forecast(rd, code, start_date):
    df = rd.req_forecast(rd, code, start_date)
    return(df)
def get_express(rd, code, start_date):
    df = rd.req_express(rd, code, start_date)
    return(df)
def profit_dedt_last_five_years(rd, code, years):
    profit_dedt = []
    profit_dedt.append(years[0])
    for i in range(len(years)):
        df = rd.req_tushare_query(rd, code, years[i])
        if( len(df) == 0 ):
            profit_dedt.append(0.0)
        else:
            profit_dedt.append(df.iloc[0]['profit_dedt'])
    return(profit_dedt)        
def pft_3_years_increase(s):
    rt = ''
    if( 'profit_dedt_years' in s.dt ):
        if(s.dt['profit_dedt_years'][1] < 0):
            rt = u'亏损'
        elif(s.dt['profit_dedt_years'][4] <= 0):
            rt = u'亏转盈'
        else:
            rt = (s.dt['profit_dedt_years'][1] / s.dt['profit_dedt_years'][4])**(1/3) - 1
            rt = round(rt, 3)
    return(rt)
def fill_flag(s):
    flag = ''
    if( hd_flag in s.flag ):
        if( s.flag[hd_flag] == 'Y' ):
            flag = 'H'
    elif( my_flag in s.flag ):
        if( s.flag[my_flag] == 'Y' ):
            flag = 'Du'
    elif( att_flag in s.flag ):
        if( s.flag[att_flag] == 'Y' ):
            flag = 'att'
    elif( len(s.flag) != 0 ):
        flag = 'com'
    else:
        flag = ''
    return(flag)

class delay_ctl():
    cnt = 0
    time_interval = 0
    freq_interval = 0
    tm_bf = []
    def init(self, cls, time_interval, freq_interval):
        cls.cnt = 0
        cls.time_interval = time_interval
        cls.freq_interval =freq_interval
        tm = datetime.datetime.now() - datetime.timedelta(seconds = time_interval * 2)
        for i in range(freq_interval):
            cls.tm_bf.append(tm)
    def ctl(self, cls):
        tm = datetime.datetime.now()
        tm_diff = cls.time_interval - (tm-cls.tm_bf[cls.cnt]).seconds
        if( tm_diff > 0 ):
            print('--- sleep: ', tm_diff, ' seconds. ---')
            time.sleep(tm_diff + 0.1)
            tm = datetime.datetime.now()
        cls.tm_bf[cls.cnt] = tm
        cls.cnt += 1
        if( cls.cnt == cls.freq_interval ):
            cls.cnt = 0
    def prt(self, cls):
        for i in range( cls.freq_interval ):
            print(cls.tm_bf[i])
class RawData():
    ts.set_token(TOKEN)
    pro = ts.pro_api()
    df_query = pd.DataFrame()
    df_stock_basic = pd.DataFrame()
    df_dividend = pd.DataFrame()
    df_balancesheet = pd.DataFrame()
    df_forecast = pd.DataFrame()
    df_express = pd.DataFrame()
    dc = delay_ctl()
    dc.init(dc, 60, 80)
    def reset(self, cls):
        cls.df_query = pd.DataFrame()
        cls.df_dividend = pd.DataFrame()
        cls.df_balancesheet = pd.DataFrame()
        cls.df_forecast = pd.DataFrame()
        cls.df_express = pd.DataFrame()
    def req_tushare(self, cls, mode, para):
        if( mode == 'query'):
            try:
                df = cls.pro.query('fina_indicator', ts_code=para[0], period=para[1])
            except Exception as e:
                print(str(e))
                os._exit(0)
        elif( mode == 'stock_basic' ):
            df = cls.pro.stock_basic(exchange='', list_status=para[0], fields=para[1])
        elif( mode == 'dividend' ):
            df = cls.pro.dividend(ts_code=get_t_s_id(para[0]), fields=para[1])
        elif( mode == 'balancesheet' ):
            df = cls.pro.balancesheet(ts_code=get_t_s_id(para[0]), start_date=para[1], end_date=get_today(), fields=para[2])
        elif( mode == 'forecast' ):
            df = cls.pro.forecast(ts_code=get_t_s_id(para[0]), start_date=para[1], end_date=para[2], fields=para[3])
        elif( mode == 'express' ):
            df = cls.pro.express(ts_code=get_t_s_id(para[0]), start_date=para[1], end_date=para[2], fields=para[3])
        else:
            df = None
            print('mode:', mode, ' not exist.')
        # sleep
        cls.dc.ctl(cls.dc)
#        time.sleep(0.76)
        return(df)
    def req_tushare_query(self, cls, code, period):
        get = False
        if(cls.df_query.shape[0] != 0):
            for i in range(cls.df_query.shape[0]):
                if( cls.df_query.iloc[i]['end_date'] == period ):
                    df = cls.df_query.iloc[[i]]
                    get = True
                    break
        if( get == False ):
            mode = 'query'
            para = []
            para.append(get_t_s_id(code))
            para.append(period)
            df = self.req_tushare(cls, mode, para)
            if( df.shape[0] != 0 ):
                cls.df_query = cls.df_query.append(df, ignore_index=True)
        return(df)
    def req_stock_basic(self, cls):
        if(cls.df_stock_basic.shape[0] == 0):
            mode = 'stock_basic'
            para = []
            para.append('L')
            para.append('symbol,area,industry,list_date')
            cls.df_stock_basic = self.req_tushare(cls, mode, para)
        return(cls.df_stock_basic)
    def req_dividend(self, cls, code):
        if(cls.df_dividend.shape[0] == 0):
            mode = 'dividend'
            para = []
            para.append(code)
            para.append('cash_div_tax,div_proc,end_date,record_date,ex_date,stk_bo_rate,stk_co_rate,stk_div')
            cls.df_dividend = self.req_tushare(cls, mode, para)
        return(cls.df_dividend)
    def req_balancesheet(self, cls, code):  
        if(cls.df_balancesheet.shape[0] == 0):
            mode = 'balancesheet'
            para = []
            para.append(code)
            para.append(last_eight_qtrs(get_today())[0])
            para.append('total_share, end_date')
            for i in range(len(last_eight_qtrs(get_today()))):
                para[1] = last_eight_qtrs(get_today())[i]
                df = self.req_tushare(cls, mode, para)
                if(df.shape[0] != 0):
                    break
            cls.df_balancesheet = df
        return(cls.df_balancesheet)
    def req_forecast(self, cls, code, start_date):  
        if(cls.df_forecast.shape[0] == 0):
            mode = 'forecast'
            para = []
            para.append(code)
            para.append(start_date)
            para.append(get_today())
            para.append('type, end_date, p_change_min, p_change_max, net_profit_min, net_profit_max')
            cls.df_forecast = self.req_tushare(cls, mode, para)
        return(cls.df_forecast)
    def req_express(self, cls, code, start_date):  
        if(cls.df_express.shape[0] == 0):
            mode = 'express'
            para = []
            para.append(code)
            para.append(start_date)
            para.append(get_today())
            para.append('ann_date, end_date, n_income, diluted_eps, yoy_tp, yoy_eps')
            cls.df_express = self.req_tushare(cls, mode, para)
        return(cls.df_express)
class Share():
    raw_data = RawData()
    def __init__(self):
        self.id = ''
        self.name =''
        self.price = 0.0
        self.flag = {}
        self.dt = {}          # 原始数据
        self.rt = {}          # 计算结果
        self.cp = {}          # 与price相关的计算结果
#    @classmethod
    def name_price_fill(self):
        self.name, self.price = get_name_price(self.id)
    def nmcard(self):
        return(self.id + '[' + self.name + ']')
    def stock_basic_fill(self, cls):
        rd = cls.raw_data
        df = rd.req_stock_basic(rd)
        for i in range(df.shape[0]):
            if( df.loc[i]['symbol'] == self.id ):
                self.dt['industry'] = df.loc[i]['industry']
                self.dt['area'] = df.loc[i]['area']
                self.dt['list_date'] = df.loc[i]['list_date']
                break
        return()
    def last_five_years_dividend(self, cls):
        dividends_last, dq_div = dividends_for_stock(cls.raw_data, self.id, get_today())
        self.dt['dividend'] = dividends_last
        for i in range(6):
            self.dt['convert'] = ['', 0.0, 0.0, 0.0]   # 转送股
            if( len(dq_div) != 0 ):
                for i in range(4):
                    if( not is_pseudo_number(dq_div[0][i]) ):
                        self.dt['convert'][i] = dq_div[0][i]
    def last_five_years_EPS(self, cls):
        year = get_last_x_years(5)
        epss = eps_these_years(cls.raw_data, self.id, year)
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
    def last_five_quarters_EPS(self, cls):
        qs_eps = eps_these_quarters(cls.raw_data, self.id)
        self.dt['EPS_qtr'] = qs_eps
        print('-----EPS_qtr------', qs_eps)
    def get_EPS_TTM(self):
        last_qtrs = last_eight_qtrs(self.dt['EPS_qtr'][0])
        if( last_qtrs[0][4:8] == '1231' ):
            eps_ttm = self.dt['EPS_qtr'][1]
            self.rt['EPS_ttm'] = round(eps_ttm, 3)
        else:
            if( is_list_number(self.dt['EPS_qtr'], 1) and (len(self.dt['EPS_qtr']) == 6) ):
                eps_q = self.dt['EPS_qtr']
                for i in range(2,6):
                    if( last_qtrs[i-1][4:8] == '1231'):
                        eps_ttm = eps_q[1] + eps_q[i] - eps_q[5]
                        break
                self.rt['EPS_ttm'] = round(eps_ttm, 3)    
            else:
                self.rt['EPS_ttm'] = 'None'
                self.flag['data'] = 'EPS_qtr'
    def get_fina_data(self, cls):
        rt = fina_indicator(cls.raw_data, self.id)
        if( 'pft_qtr' in rt ):
            self.dt['profit_dedt_qtrs'] = rt['pft_qtr']
        else:
            self.dt['profit_dedt_qtrs'] = 0
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
    def get_total_share(self):              # 总股本
        rd = RawData()
        df = rd.req_balancesheet(rd, self.id)
        if( not is_pseudo_number(df.iloc[0]['total_share']) ):
            self.dt['total_share'] = df.iloc[0]['total_share']
        else:
            self.dt['total_share'] = None
    def get_base(self, cls):
        self.name_price_fill()
        self.stock_basic_fill(cls)
        self.last_five_years_dividend(cls)
        self.last_five_years_EPS(cls)
        self.last_five_quarters_EPS(cls)
        self.get_EPS_TTM()
        self.get_fina_data(cls)
        self.get_total_share()
        self.profit_dedt(cls)
    def calc(self):
        self.calc_lfy_div_rate()
        self.get_EPS_TTM()
        self.rt['income_up'] = calc_income_up(self.dt['dividend'])
        self.rt['profit_dedt_acc'] = calc_pft_acc(self.dt['profit_dedt_qtrs'])                         # 净利润季报增速
        self.rt['gold_include'] = calc_gold_include(self.dt['ocfps'], self.dt['eps'])
        self.rt['convert_rate'] = calc_convert_rate(self.dt['convert'])
        self.rt['avg_div_rate'] = calc_avg_div_rates(self.rt['div_rate'])
        self.rt['last_year_div'] = round( self.dt['dividend'][1]/self.rt['convert_rate'], 3)           # 最新年度分红
    def calc_cp(self):
        self.cp['stk_div_ratio'] = calc_stk_div_ratio(self.price, self.dt['dividend'], self.rt['convert_rate'])   # 当前股息率
        self.cp['hope_div'] = round(self.price * hope_dividend_ratio, 3)          # 期望保底分红
        if( (self.rt['EPS_ttm'] != 0) and is_number(self.rt['EPS_ttm']) ):
            self.cp['safe_div'] = round( self.cp['hope_div']/self.rt['EPS_ttm'], 3)           # 保底分红率 = 期望保底分红 /EPS_TTM
        else:
            self.cp['safe_div'] = 'None'           # 保底分红率 = 期望保底分红 /EPS_TTM
        self.cp['div_status'] = calc_div_status(self.cp['safe_div'], self.rt['avg_div_rate'])
    def forecast(self, cls):
        start_date = other_day(self.dt['profit_dedt_qtrs'][0], 1)
        df = get_forecast(cls.raw_data, self.id, start_date)
        return(df)
    def express(self, cls):
        start_date = other_day(self.dt['profit_dedt_qtrs'][0], 1)
        df = get_express(cls.raw_data, self.id, start_date)
        return(df)
    def profit_dedt(self, cls):
        years = get_last_x_years(5)
        req = False
        if( 'profit_dedt_years' in self.dt ):
            if( self.dt['profit_dedt_years'][0] != get_last_x_years(5)[0] ):
                req = True
        else:
            req = True
        if( req ):    
            profit_dedt = profit_dedt_last_five_years(cls.raw_data, self.id, years)
            self.dt['profit_dedt_years'] = profit_dedt

    
    