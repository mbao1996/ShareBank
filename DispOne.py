#coding=gbk
from define import *
from lib import *

fn = work_catalog + bank_name
ShareBank = read_data(fn)

code = '000895'
flag = ''
count = 0

for i in range( len(ShareBank) ):
    s = ShareBank[i]
    if( s.id == code ):
        count += 1
        print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
        print(s.dt['profit_dedt_years'])
        print('   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)
    if( flag in s.flag ):
        count += 1
        print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
        print('   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)

print(count, '\n finished')
