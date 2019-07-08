#coding=gbk
import tushare
import os
from openpyxl import load_workbook
from define import *
from lib import *
from _tracemalloc import start

fn = work_catalog + bank_name 
fn_wr = work_catalog + '\DivRatio.xlsm'
print('   ***   tushare_version: ', tushare.__version__, '   ***\n')

ShareBank = read_data(fn)

ts.set_token(TOKEN)
pro = ts.pro_api()
s = ShareBank[8]
s.get_total_share(s)
'''
rd = RawData()
df = rd.req_dividend(rd, s.id)
print(df)
print(df.iloc[1]['div_proc'])
'''
#df = pro.balancesheet(ts_code=get_t_s_id(s.id), start_date=last_eight_qtrs(get_today())[1], end_date=get_today(), fields='total_share, ann_date, f_ann_date, end_date')
#print(df.shape[0],'\n\n', df)

'''
for i in range(10):
    s = ShareBank[i]
#    s.prt()
#    s.stock_basic_fill()
    print(s.id,'[', s.name,']', s.dt['industry'], s.dt['area'], s.dt['list_date'])
'''    
    
print('\n finished')
