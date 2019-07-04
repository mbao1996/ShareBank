#coding=gbk
from define import *
from lib import *

fn = work_catalog + bank_name
ShareBank = read_data(fn)

flag_before = 'no'
flag_after = 'holding'
to_add = ['', 'goodu']
to_del = ['', 'holding']
batch_add = 'attention'

count = 0
for i in range( len(ShareBank) ):
    s = ShareBank[i]
    if( flag_before in s.flag ):
        count += 1
        s.flag[flag_after] = s.flag[flag_before]
        del s.flag[flag_before]
        print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
        print('   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)
    if( s.id == to_add[0] ):
        count += 1
        s.flag[to_add[1]] = 'Y'
        print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
        print('   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)
    if( s.id == to_del[0] and to_del[1] in s.flag ):
        count += 1
        del s.flag[to_del[1]]
        print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)
        print('   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)

    batch_add_flag = False
#    batch_add_flag = 'holding' in s.flag or 'goodu' in s.flag
    if(batch_add_flag):
        count += 1
        s.flag[batch_add] = 'Y'
        print(i, '[max:', len(ShareBank), ']: ', s.nmcard(), '---flag---:', s.flag)

print(count)        
save_data(fn, ShareBank)
print('\n finished')
