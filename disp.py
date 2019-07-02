#coding=gbk
from define import *
from lib import *

fn = work_catalog + bank_name
ShareBank = read_data(fn)

row_start = 0             # adjustable
row_end = 3            # adjustable

if( row_end > len(ShareBank) ):
    row_end = len(ShareBank)
for i in range( row_start, row_end ):
    s = ShareBank[i]
    print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
    print('   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)

print('\n finished')
