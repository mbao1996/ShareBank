#coding=gbk
from define import *
from lib import *

fn = work_catalog + bank_name
ShareBank = read_data(fn)
s = Share()
s.id = '300176'

share_del(ShareBank, '600309')
#share_add(ShareBank, s)

for i in range( len(ShareBank) ):
    s = ShareBank[i]
    
#    s.stock_basic_fill()
#    s.name_price_fill()
#    s.last_five_years_dividend(s)
#    s.last_five_years_EPS(s)
#    s.calc_lfy_div_rate()
#    s.last_five_quarters_EPS(s)
#    s.get_EPS_TTM()
#    s.get_fina_data(s)
#    s.get_net_income(s)
#    s.get_total_share(s)
#    s.test(s)
#    s.calc()
#    s.name_price_fill()
#    s.calc_cp()
    print(i, ': ', s.nmcard(),'\n   ', s.dt,'\n   ', s.rt,'\n   ', s.cp)
save_data(fn, ShareBank)
print('\n finished')
