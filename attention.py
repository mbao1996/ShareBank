#coding=gbk
import tushare
import os
from define import *
from lib import *

fn = work_catalog + bank_name 
print('   ***   tushare_version: ', tushare.__version__, '   ***\n')

ShareBank = read_data(fn)

flag = ['goodu', 'holding']
cnt = 0
for i in range(len(ShareBank)):
    s = ShareBank[i]
    if( has_flag(s, flag) ):
        s.forecast(s)
#        s.express()
        cnt += 1
#        print(s.nmcard(), s.flag)
        
print(cnt)
    
print('\n finished')
