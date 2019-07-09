#coding=gbk
import tushare
import os
from openpyxl import load_workbook
from define import *
from lib import *

fn = work_catalog + bank_name 
fn_wr = work_catalog + '\DivRatio.xlsm'
print('   ***   tushare_version: ', tushare.__version__, '   ***\n')

ShareBank = read_data(fn)

flag = ['goodu', 'holding']
def has_flag(s, flag):
    has = False
    for i in range(len(flag)):
        if( flag[i] in s.flag ):
            if( s.flag[flag[i]] == 'Y' ):
                has = True
    return(has)    


ts.set_token(TOKEN)
pro = ts.pro_api()
#s = ShareBank[8]
cnt = 0
for i in range(len(ShareBank)):
    s = ShareBank[i]
    if( has_flag(s, flag) ):
        df = s.express(s)
        cnt += 1
        if( df.shape[0] != 0 ):
            for j in range(df.shape[0] ):
                if( df.iloc[j]['end_date'] == '20190630'):
                    print(s.nmcard(), s.flag)
                    print(df)
        if( cnt >= 99 ):
            break
print(cnt)


'''
s.get_total_share(s)
rd = RawData()
df = rd.req_dividend(rd, s.id)
print(df)
print(df.iloc[1]['div_proc'])

#df = pro.balancesheet(ts_code=get_t_s_id(s.id), start_date=last_eight_qtrs(get_today())[1], end_date=get_today(), fields='total_share, ann_date, f_ann_date, end_date')
#print(df.shape[0],'\n\n', df)

for i in range(10):
    s = ShareBank[i]
    print(s.id,'[', s.name,']', s.dt['industry'], s.dt['area'], s.dt['list_date'])
'''    
    
print('\n finished')
