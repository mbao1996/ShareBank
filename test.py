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
s = ShareBank[23]
print(s.dt['EPS_qtr'])
print(s.rt['EPS_ttm'])
s.get_EPS_TTM()
print(s.rt['EPS_ttm'])

'''
start = 0
#end = len(ShareBank)
end = 1
for i in range(start, end):
    s = ShareBank[i]
    s.dt['profit_dedt_qtrs'] = s.dt['profit_dedt']
    del s.dt['profit_dedt']
#save_data(fn, ShareBank)

ts.set_token(TOKEN)
pro = ts.pro_api()
mode = 'query'
para = []
para.append('600036.SH')
para.append('20181231')
print(para)
df = req_tushare(pro, mode, para)
print('+++++', len(df))
if( len(df) != 0 ):
    print(df['end_date'][0])
    print(df.iloc[0]['ann_date'])
else:
    print('no return')

ShareBank = read_data(fn)
try:
    wb = load_workbook(fn_wr,keep_vba=True)
except Exception as e:
    print(str(e))
    os._exit(0)
ws = wb['Sheet1']

my_flag = 'goodu'
hd_flag = 'holding'

count = 1
for i in range( len(ShareBank) ):
    s = ShareBank[i]
    req = False
    if( my_flag in s.flag or hd_flag in s.flag ):
        if( hd_flag in s.flag ):
            if( s.flag[hd_flag] == 'Y' ):
                req = True
        if( my_flag in s.flag ):
            if( s.flag[my_flag] == 'Y' ):
                req = True
        if( req ):
#            s.forecast(s)
            print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
            s.express(s)
            count += 1
            if( count % 10 == 0 ):
                print('*** nap now *** ', end='')
                for k in range(10):
                    print( k+1, ' ', end='')
                    time.sleep(3)
                print('')
#wb.save(fn_wr)
'''
print('\n finished')
