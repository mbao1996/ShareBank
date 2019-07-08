# -*- coding: utf-8 -*-
#coding=gbk
import time
from define import *
from lib import *

fn = work_catalog + bank_name
ShareBank = read_data(fn)
flag = 'attention'
cnt = 0
row_start = 0     # adjustable
for i in range(row_start, len(ShareBank)):
    s = ShareBank[i]
    rd = RawData()
    rd.reset(rd)
    if( flag in s.flag ):
        cnt += 1
#        s.name_price_fill()
#        s.calc_cp()
#        s.profit_dedt(s)
        print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
#    s.get_base()
        s.calc()
        s.calc_cp()
#        save_data(fn, ShareBank)
#save_data(fn, ShareBank)

print(cnt, '\n finished')
