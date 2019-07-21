#coding=gbk
from define import *
from lib import *

fn = work_catalog + bank_name
ShareBank = read_data(fn)

row_start = 0             # adjustable
row_end = 4000            # adjustable

if( row_end > len(ShareBank) ):
    row_end = len(ShareBank)
for i in range( row_start, row_end ):
    s = ShareBank[i]
    if( s.dt['profit_dedt_qtrs'][0] == last_qtr(get_today()) ):
        print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
        print('   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)

print('\n finished')
