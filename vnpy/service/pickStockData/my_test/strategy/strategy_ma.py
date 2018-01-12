# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 17:11:49 2017

@author: chen
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 09:59:20 2017

@author: chen
采用均线选股策略
"""

"""This script parse stock info"""

import tushare as ts
#import pymongo
import json
import datetime #导入日期时间模块
import pymongo
import pprint
import numpy as np
import pandas as pd
import talib as ta
from pymongo import MongoClient


def select_by_basic_policy(collection_select, basic_record, today_record, weight):
    '''策略'''

    close = today_record['close']

    #3倍
    #每股净资产
    #每股未分配利润
    #每股公积金
    base = basic_record['bvps'] + basic_record['perundp'] + basic_record['reservedPerShare']
    if close < (weight * base):
        code = basic_record['code']
        print(code)
        new_records = {"code": code,
              "close": close,
              "weight": weight,
              "base": base,
              "bvps": basic_record['bvps'],
              "perundp": basic_record['perundp'],
              "reservedPerShare": basic_record['reservedPerShare']}
        collection_select.insert_one(new_records)

    return

def select_by_basic():
    '''保存今天的k数据'''

    client = MongoClient("localhost", 27017)

    today = '2017-07-19'
    #today = datetime.date.today() #获得今天的日期
    collection_records = client.basic_report.records
    db_week = client.week
    #print(collection)


    # 创建迭代器对象, 遍历列表
    list_name = collection_records.find()
    for item in list_name:
        #创建股票代码命名的集合
        #print(item)

        #print(item['code'])
        code = item['code']
        #print(code)


        collection_code = db_week[code]
        #print(collection_code)

        #今天的收盘价
        today_record = collection_code.find_one({'date':str(today)})
        #print(today_record)
        if today_record is not None:
            #基本面3倍选股
            select_by_basic_policy(client.basic_report.select_result, item, today_record, 1)
        #保存数据
    return

"""""entry"""""
if __name__ == '__main__':
    select_by_basic()