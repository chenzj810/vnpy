# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:08:08 2017

@author: chen
"""

from dataRecorder.download_hist_data import save_today_data,save_basic_report
from strategy.strategy_basic import select_by_basic
import datetime #导入日期时间模块

today = datetime.date.today() #获得今天的日期
print(today)

#更新今天数据
save_today_data('all')
save_basic_report()

#选股
select_by_basic()
