#coding=gbk
import tushare
import os
from define import *
from lib import *

fn = work_catalog + bank_name 
print('   ***   tushare_version: ', tushare.__version__, '   ***\n')

ShareBank = read_data(fn)

flag = ['goodu', 'holding']
seek_date = last_qtr(get_today())
if( seek_date[4:8] == '0331' ):
    year = str(int(seek_date[0:4])-1)
    seek_date = year + '1231'

cnt = 0
for i in range(len(ShareBank)):
    s = ShareBank[i]
    if( has_flag(s, flag) ):
#        print(i, '---', s.nmcard())
        cnt += 1
        df = s.forecast(s)
        if( df.shape[0] != 0 ):
            for j in range(df.shape[0] ):
                if( df.iloc[j]['end_date'] == seek_date ):
                    print('[',i,']---forecast---', s.nmcard(), s.flag)
                    print(df)
        df = s.express(s)
        if( df.shape[0] != 0 ):
            for j in range(df.shape[0] ):
                if( df.iloc[j]['end_date'] == seek_date ):
                    print('[',i,']---express---', s.nmcard(), s.flag)
                    print(df)
        
print(cnt)
  
print('\n finished')
