# -*- coding: utf-8 -*-
#coding=gbk
import time
from define import *
from lib import *

fn = work_catalog + bank_name
ShareBank = read_data(fn)

flag = ['goodu', 'holding']
cnt = 0
row_start = 2060    # adjustable
for i in range(row_start, len(ShareBank)):
    s = ShareBank[i]
    s.raw_data.reset(s.raw_data)
    s.flag['data'] = 'right'
#    if( has_flags(s, flag) ):
    if( s.dt['profit_dedt_qtrs'][0] != last_qtr(get_today()) ):
        cnt += 1
        s.name_price_fill()
        s.get_base(s)
        s.calc()
        s.calc_cp()
        print('(',cnt,')', i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
        print('   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)
        save_data(fn, ShareBank)
    else:
        print('***skip*** (',cnt,')', i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)

#save_data(fn, ShareBank)
print(cnt)

print('\n finished')
