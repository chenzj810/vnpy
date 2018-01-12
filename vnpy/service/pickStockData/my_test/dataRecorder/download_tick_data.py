#!/usr/bin/python  
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 09:59:20 2017

@author: chen
"""

"""This script parse stock info"""  

""" import tushare as ts import time import queue import threading import pandas as ps from sqlalchemy import create_engine THREADS_NUM = 25 # 采集线程数 THREADS_EXITFLAG = 0 # 线程退出标志 TICKS_DATA_DATE = '2017-01-04' # 指定采集日期 MYSQL_ENGINE = 'mysql://root:pwd@ip:port/dbname?charset=utf8' class GetStockData(threading.Thread): def __init__(self, threadID, q): threading.Thread.__init__(self) self.threadID = threadID self.q = q def run(self): print ('线程%s开始下载' % (self.threadID)) self._process_data() def _process_data(self): engine = create_engine(MYSQL_ENGINE) while not THREADS_EXITFLAG: if not self.q.empty(): code = self.q.get() remain_num = self.q.qsize() tick_data = get_tick(code, TICKS_DATA_DATE) #根据当请求的股票当日停牌时，返回的数据有三行 if len(tick_data) > 3: save_to_mysql(TICKS_DATA_DATE, tick_data, engine, code, remain_num) time.sleep(0.05) else: break def get_stock_basics(): """
    获取当日股票列表
    Return
    --------
    DataFrame
    """ basics = ts.get_stock_basics() return basics def get_tick(stockCode=None, date=None): """
    根据股票列表的股票代码获取当日/指定日期历史分笔
    Return
    --------
    DataFrame
    """ tick_data = '' if date != None and date != '': tick_data = ts.get_tick_data(stockCode, date) else: tick_data = ts.get_today_ticks(stockCode) if not tick_data.dropna(axis=0, how='any', thresh=None).empty: tick_data.insert(0, 'code', stockCode) #插入股票代码字段 return tick_data def save_to_mysql(tablename=None, data=None, engine=None, code=None, num=None): """
    保存获取的数据到MySQL数据库中
    Return
    --------
    """ for i in range(3): try: data.to_sql(tablename, engine, if_exists='append') print('save %s %s' % (code, num)) break except BaseException as e: print ('Save Error %s ' % (code)) return def main(): #    reload(sys) #    sys.setdefaultencoding('utf8') stock_codes = get_stock_basics() threads = [] try: """
        根据股票代码列表创建队列
        """ stocks = queue.Queue(len(stock_codes)) for code in stock_codes.index: code = str(code) if (len(code) != 6): code = (6 - len(code)) * '0' + code stocks.put(code) """
        创建并运行线程
        """ for n in range(THREADS_NUM): thread = GetStockData(n, stocks) thread.start() threads.append(thread) while not stocks.empty(): pass print ('数据请求完毕。') THREADS_EXITFLAG = 1 for t in threads: t.join() except BaseException as e: print ('Error', e) return if __name__ == '__main__': print ('开始请求％s的数据' % (TICKS_DATA_DATE)) main()

作者：转工
链接：http://www.jianshu.com/p/31452e5da5ee
來源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。