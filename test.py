#coding=gbk
from define import *
from lib import *
import tushare

print(tushare.__version__)

fn = work_catalog + bank_name
ShareBank = read_data(fn)


s = Share()
s.id = '000001'

d = {'t':1, 'tt':2, 'ttt':3}
d.pop('tt')
print(d)

      
      
      
#share_add(ShareBank, s)

#share_del(ShareBank, '002500')
#share_add(ShareBank, s)

#for i in range( len(ShareBank) ):
#    s = ShareBank[i]
#    s.flag['watch'] = 'Y'
#    print(i, ': ', s.nmcard(), '--watch---:', s.flag['watch'])
#    print('   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)

#save_data(fn, ShareBank)
print('\n finished')
