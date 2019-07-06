# -*- coding: utf-8 -*-
#coding=gbk
import time
from define import *
from lib import *

fn = work_catalog + bank_name
ShareBank = read_data(fn)
flag = 'goodu'
row_start = 0     # adjustable

for i in range(row_start, len(ShareBank)):
    s = ShareBank[i]
    rd = RowData()
    rd.reset()
    if( flag in s.flag ):
        s.name_price_fill()
        s.calc_cp()
        print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)

#    s.get_base()
#    s.calc()
#    s.calc_cp()
#    save_data(fn, ShareBank)
    '''
    print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
    print('   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)
    if( i%5 == 0 ):
        print('******** nap now ******** ', end='')
        for k in range(15):
            print( k+1, ' ', end='')
            time.sleep(5)
        print('')
    '''
save_data(fn, ShareBank)
print('\n finished')
