# -*- coding: utf-8 -*-

import time
from define import *
from lib import *

fn = work_catalog + bank_name
ShareBank = read_data(fn)

my_flag = 'goodu'

code = '600566'    
if( len(ShareBank) != 0 ):
    for i in range(len(ShareBank)):
        if( ShareBank[i].id == code):
            ShareBank[i].flag[my_flag] = 'Y'
            print(ShareBank[i].name, ' --- Done ---')
            break
    
    save_data(fn, ShareBank)
print('\n finished')
