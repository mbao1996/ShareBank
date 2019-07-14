# -*- coding: utf-8 -*-
#coding=gbk
import time
from define import *
from lib import *

fn = work_catalog + bank_name
ShareBank = read_data(fn)

flag = ['goodu', 'holding']
cnt = 0
row_start = 34     # adjustable
for i in range(row_start, len(ShareBank)):
    s = ShareBank[i]
    s.raw_data.reset(s.raw_data)
#    if( has_flag(s, flag) ):
    if( True ):
        cnt += 1
        s.name_price_fill()
        s.get_base(s)
        s.calc()
        s.calc_cp()
        print('(',cnt,')', i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
        print('   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)
        save_data(fn, ShareBank)
#save_data(fn, ShareBank)
print(cnt)

print('\n finished')
