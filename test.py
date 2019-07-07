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
#s = ShareBank(6)

for i in range(10):
    s = ShareBank[i]
#    s.prt()
    s.stock_basic_fill()
#    s.prt()
    print(s.id,'[', s.name,']', s.dt['industry'], s.dt['area'], s.dt['list_date'])
    
    
print('\n finished')
