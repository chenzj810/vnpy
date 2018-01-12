#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 09:59:20 2017

@author: chen
@version:
@see:
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

#基本面选股的最大倍数
BASE_OF_MAX_WEIGHT = 1

"""
function
@param collection_select: 数据库
@param basic_record: 基本面数据集合
@param today_record: 选定日期的数据集合
@param weight: 权重，基本面的倍数
"""

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


"""
function
@param db_data: 数据库
@param collection_base: 基本面数据集合
@param date: 日期
@param collection_result: 结果输出数据集合
"""

def select_by_basic_db(db_data, collection_base, date, collection_result):
    '''根据日线数据和基本面数据选股'''


    # 创建迭代器对象, 遍历列表
    list_name = collection_base.find()
    for item in list_name:
        #创建股票代码命名的集合
        #print(item)

        #print(item['code'])
        code = item['code']
        #print(code)


        collection_code = db_data[code]
        #print(collection_code)


        #周六，周日时，节假日时，往前找有数据的天进行选股
        for i in range(0, -10, -1):
            delta = datetime.timedelta(days=i)
            my_date = str(date + delta)
            #print(my_date)

             #今天的记录收盘价
            today_record = collection_code.find_one({'date':my_date})
            if today_record is not None:
                #print(today_record)

                #基本面3倍选股
                select_by_basic_policy(collection_result, item, today_record, BASE_OF_MAX_WEIGHT)
                break;

        #退出
    return

"""
@function:select_by_basic
@param void:
@return void:
@rtype void:
"""
def select_by_basic():
    '''今天的k数据进行选股'''

    client = MongoClient("localhost", 27017)

    #根据今天的日k 线数据进行选股
    today = datetime.date.today() #获得今天的日期

    #collection 数据集合
    collection_basic = client.basic_report.records
    collection_result = client.select_result.basic_env
    my_db = client.day
    #print(collection)


    #删除上次选股的全部记录
    collection_result.remove()

    #重新选股
    select_by_basic_db(my_db, collection_basic, today, collection_result)
    return

def test():
    """测试函数"""
    select_by_basic()


"""""entry"""""
if __name__ == '__main__':
    test()