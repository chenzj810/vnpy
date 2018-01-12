# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:16:10 2017

@author: chen
"""

import datetime
import time

today =datetime.date.today()

localtime = time.localtime(time.time())

print('today:', today)
print('localtime:', localtime)
print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print (time.strftime("%H:%M:%S", time.localtime()))

struct_time = time.strptime("18:19:05", "%H:%M:%S")
print(struct_time)