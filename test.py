#coding=gbk
import tushare
import os
from openpyxl import load_workbook
from define import *
from lib import *

fn = work_catalog + bank_name 
fn_wr = work_catalog + '\DivRatio.xlsm'
print('   ***   tushare_version: ', tushare.__version__, '   ***\n')

ts.set_token(TOKEN)
pro = ts.pro_api()
mode = 'query'
para = []
para.append('600036.SH')
para.append('20181231')
print(para)
df = req_tushare(pro, mode, para)
if( len(df) != 0 ):
    for dfr in df.iterrows():
        dt = dfr[1]
        print(dt)
else:
    print('no return')
'''
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
