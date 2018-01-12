#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 09:59:20 2017

@author: chen
"""

"""This script parse stock info"""

import tushare as ts
#import pymongo
import json
import datetime #导入日期时间模块
import pymongo
import pprint
#import errors
#import numpy as np
import pandas as pd
from pymongo import MongoClient

#print(ts.__version__)


def delete_repeat_data():

    client = pymongo.MongoClient('localhost', 27017)
    db = client.local
    collection = db.person

    for url in collection.distinct('name'):#使用distinct方法，获取每一个独特的元素列表
        num= collection.count({"name":url})#统计每一个元素的数量
        print (num)
        for i in range(1,num):#根据每一个元素的数量进行删除操作，当前元素只有一个就不再删除
            print ('delete %s %d times '% (url, i))
            #注意后面的参数， 很奇怪，在mongo命令行下，它为1时，是删除一个元素，这里却是为0时删除一个
            collection.remove({"name":url}, 0)
        for i in  collection.find({"name":url}):#打印当前所有元素
            print (i)
    print (collection.distinct('name'))#再次打印一遍所要去重的元素

def delete_single_database_repeat_data():

    client = pymongo.MongoClient('localhost', 27017)
    db=client.GifDB #这里是将要清洗数据的数据库名字
    for table in  db.collection_names():
        print ('table name is ',table)
        collection=db[table]
        for url in collection.distinct('gif_url'):#使用distinct方法，获取每一个独特的元素列表
            num= collection.count({"gif_url":url})#统计每一个元素的数量
            print (num)
            for i in range(1,num):#根据每一个元素的数量进行删除操作，当前元素只有一个就不再删除
                print ('delete %s %d times '% (url,i))
                #注意后面的参数， 很奇怪，在mongo命令行下，它为1时，是删除一个元素，这里却是为0时删除一个
                collection.remove({"gif_url":url},0)
            for i in  collection.find({"gif_url":url}):#打印当前所有元素
                print (i)




def clear_coll_datas(db, collection):
    #清空一个集合中的所有数据
    db[collection].remove({})
    array = list(db.test_collection.find())
    pprint.pprint(array)





def add_null_data(db, mytype):
    '''添加数据库中collection为空的数据'''

    #获取所有股票列表
    stock_list = ts.get_stock_basics().index

    it = iter(stock_list)    # 创建迭代器对象
    for code in it:
        #创建股票代码命名的集合
        collection = db[code]


        result = collection.find_one()
        #print('代码：' + code)
        if result is None:
            print('代码：' + code)
            df = ts.get_k_data(code, ktype=mytype)
            if df.empty:
                print("null")
                break

            #print(df)
            collection.insert_many(json.loads(df.to_json(orient='records')))

    return



"""
@function save the data of k
@parameter db: database
@parameter mytype: the type of k
"""
def save_ktype_data(db, mytype):
    '''保存数据'''

    #获取所有股票列表
    stock_list = ts.get_stock_basics().index

    it = iter(stock_list)    # 创建迭代器对象
    for code in it:
        #print (code, end=" ")

        #创建股票代码命名的集合
        collection = db[code]

        #创建唯一索引，并消除重复数据。
        #collection.drop_index([("date", pymongo.ASCENDING)])
        try:
            collection.create_index([("date", pymongo.ASCENDING)], unique=True, dropDups=True)
        except:
            pass

        print('代码：' + code + '  mytype:' + mytype)
        try:
            df = ts.get_k_data(code, ktype=mytype)
            if df.empty:
                print("null")
                continue

            #重复的数据，忽略
            collection.insert(json.loads(df.to_json(orient='records')), continue_on_error=True)
        except pymongo.errors.DuplicateKeyError:
            print("DuplicateKey")
        except pymongo.errors.BulkWriteError:
            print("BulkWriteError")
    return


"""
@function save all the data
"""
def save_all_data(data_type):

    #连接mongodb数据库
    client = MongoClient("localhost", 27017)

    if data_type == 'M' or data_type == 'all':
        save_ktype_data(client.month, 'M')
    if data_type == 'W' or data_type == 'all':
        save_ktype_data(client.week, 'W')
    if data_type == 'D' or data_type == 'all':
        save_ktype_data(client.day, 'D')
    if data_type == '60' or data_type == 'all':
        save_ktype_data(client.mintue60, '60')
    if data_type == '30' or data_type == 'all':
        save_ktype_data(client.mintue30, '30')
    if data_type == '15' or data_type == 'all':
        save_ktype_data(client.mintue15, '15')
    if data_type == '5' or data_type == 'all':
        save_ktype_data(client.mintue5, '5')
    return

"""
@function save the data of k at today
@parameter db: database
@parameter mytype: the type of k
@parameter date: the date
"""
def save_today_k_data(code, db, mytype, date):

    #创建股票代码命名的集合
    collection = db[code]

    #创建唯一索引，并消除重复数据。
    #collection.drop_index([("date", pymongo.ASCENDING)])
    try:
        collection.create_index([("date", pymongo.ASCENDING)], unique=True, dropDups=True)
    except:
        pass

    print('save_today_k_data; mytype:' + mytype + '  code:' + code + '  date:' + date)
    try:
        df = ts.get_k_data(code, ktype=mytype, start=date, end=date)
        #print(df)
        if df.empty:
            print("data is null")
        else:
            #重复的数据，忽略
            #print("insert_one data")
            #print(df)
            collection.insert(json.loads(df.to_json(orient='records')), continue_on_error=True)
    except pymongo.errors.DuplicateKeyError:
        print("DuplicateKey")
    return


"""
@function :save the data at today
"""
def save_today_data(data_type):
    '''保存今天的k数据'''

    client = MongoClient("localhost", 27017)
    today =datetime.date.today()  #获得今天的日期
    delta = datetime.timedelta(days=-1)
    my_date = str(today + delta)

    #获取所有股票列表
    stock_list = ts.get_stock_basics().index

    it = iter(stock_list)    # 创建迭代器对象
    for code in it:
        #创建股票代码命名的集合
        collection = client.day[code]

        #query = {'date':str(my_date)}
        result = collection.find_one({'date':my_date})
        #print('代码：' + code)
        if result is not None:
            continue

        #保存数据
        #print('代码：' + code)
        if data_type == 'D' or data_type == 'all':
            save_today_k_data(code, client.day, 'D', my_date)
        if data_type == '60' or data_type == 'all':
            save_today_k_data(code, client.mintue60, '60', my_date)
        if data_type == '30' or data_type == 'all':
            save_today_k_data(code, client.mintue30, '30', my_date)
        if data_type == '15' or data_type == 'all':
            save_today_k_data(code, client.mintue15, '15', my_date)
        if data_type == '5' or data_type == 'all':
            save_today_k_data(code, client.mintue5, '5', my_date)

        #如果今天是星期天
        if (today.timetuple().tm_wday == 6) and (data_type == 'W' or data_type == 'all'):
            save_today_k_data(code, client.week, 'W', my_date)

        #如果今天是1号,保存月线数据
        if (today.timetuple().tm_mday == 1) and (data_type == 'M' or data_type == 'all'):
            save_today_k_data(code, client.month, 'M', my_date)

    return

"""
@function :save the data of basic report
"""
def save_basic_report():
    '''保存今天的基本面数据'''

    client = MongoClient("localhost", 27017)

    #获取所有股票基本信息
    df = ts.get_stock_basics()
    collection = client.basic_report.records
    #print(df)
    #code=df.index

    #增加code的列，在原df中code是行index
    df['code'] = pd.Series(df.index, index=df.index)
    #创建唯一索引，并消除重复数据。防重复数据
    try:
        collection.create_index([("code", pymongo.ASCENDING)], unique=True, dropDups=True)
    except:
        pass

    try:
        collection.insert(json.loads(df.to_json(orient='records')))
    except pymongo.errors.DuplicateKeyError:
        print("DuplicateKey")
    return


"""
@function :test function
"""
def test_add_datas():
    '''test_add_datas'''

    client = MongoClient("localhost", 27017)
    db=client.test
    collection = db['000797']
    df = ts.get_k_data('000797')

    print(collection.name)
    #print(collection.index_information())

    #创建唯一索引，并消除重复数据。
    #collection.ensure_index({"date":1},{"unique":True,"dropDups":True})
    #index = pymongo.IndexModel([("date", pymongo.ASCENDING)])
    #collection.drop_index([("date", pymongo.ASCENDING)])
    #print(collection.index_information())
    collection.create_index([("date", pymongo.ASCENDING)], unique=True, dropDups=True)
    print(df)
    try:
        #重复的数据，忽略
        collection.insert(json.loads(df.to_json(orient='records')))
        #collection.update_many(json.loads(df.to_json(orient='records')))
    except pymongo.errors.DuplicateKeyError:
        print("DuplicateKey")

    #print(df.to_json(orient='records'))

    result = collection.find_one()
    print(result)
    return

"""""entry"""""
if __name__ == '__main__':

    #test_add_datas()
    #save_all_data('D')

    #save_today_data('all')
    save_basic_report()
