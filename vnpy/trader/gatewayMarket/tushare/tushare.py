# encoding: UTF-8

'''
vn.stub的gateway接入
'''



from vnpy.trader.gatewayMarket.vtMarket import VtMarket
from vnpy.trader.main.vtObject import VtLogData, VtTickData
from vnpy.trader.gatewayTrade.vtGateway import *
from vnpy.trader.language.vtConstant import *
from vnpy.trader.event.eventEngine import EventEngine
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import threading
import tushare as ts
#import pymongo
import json
import datetime #导入日期时间模块
import pymongo
#import errors
#import numpy as np
import pandas as pd
from pymongo import MongoClient



########################################################################
class TushareDataApi(VtMarket):
    """数据接口接口，使用tushare实时数据接口"""

    #----------------------------------------------------------------------
    def __init__(self, eventEngine, dbClient=None):
        """Constructor"""

        super(TushareDataApi, self).__init__(eventEngine, dbClient)
        if dbClient != None:
            #self.gateway = gatewayName
            self.dbClient = dbClient
        #super(WudituDataApi, self).__init__()

        self.market = 'tushare'
        print('TushareDataApi:', dbClient)



        # tick数据字典， key：code v: tickdata
        self.tickDict = {}     # 股票代码列表
        self.tickCodeList = []     # 股票代码列表



        self.stockDict = {}     # 股票代码列表


        self.timerRun = False

        # 股票标的字典
        self.save_basic_report(self.dbClient)

        # timer处理线程
        '''
        self.__tickTimerPeriod = 5   # 5 second
        self.__tickTimer = threading.Timer(self.__tickTimerPeriod, self.__onTimer)
        self.__tickTimer.setDaemon(True)
        #self.__tickTimer.join()
        self.__tickTimer.start()
        print('tickTimer start!, isDaemon:', self.__tickTimer.isDaemon())
        '''


    #----------------------------------------------------------------------
    def __del__(self):
        self.onStop()


    #----------------------------------------------------------------------
    def __onTimer(self):

        """引擎运行"""
        #print('Hello Timer!', self.__tickTimer.isDaemon())
        self.onTick()

        if len(self.tickCodeList) == 0:
            self.onStop()
            return

        # start timer
        self.__tickTimer = threading.Timer(self.__tickTimerPeriod, self.__onTimer)
        self.__tickTimer.setDaemon(True)
        self.__tickTimer.start()

    #----------------------------------------------------------------------
    def onStart(self):


        # timer处理线程
        if self.timerRun == False:
            self.__tickTimerPeriod = 16   # 5 second
            self.__tickTimer = threading.Timer(self.__tickTimerPeriod, self.__onTimer)
            self.__tickTimer.setDaemon(True)
            #self.__tickTimer.join()
            self.__tickTimer.start()
            self.timerRun = True

        print('tickTimer start!, isDaemon:', self.__tickTimer.isDaemon())

    #----------------------------------------------------------------------
    def onStop(self):
        if self.timerRun == True:
            self.__tickTimer.cancel()
            self.timerRun = False
        print('tickTimer cancel!')



    #----------------------------------------------------------------------
    def onUpdate(self, action, code):
        """更新任务"""

        if action == 'add':
            self.tickCodeList.append(code)

            # list去重，set
            self.tickCodeList = list(set(self.tickCodeList))

            # 同步获取今天所有的数据
            #df = self.onSyncTicks(code)
        elif action == 'del':
            try:
                self.tickCodeList.remove(code)
            except:
                pass

        print(action, 'gateway, tickCodeList:', self.tickCodeList)


    #----------------------------------------------------------------------
    def onTick(self):
        """实时深度推送, 默认按照5秒1次"""

        if self.tickCodeList == []:
            print("tickCodeList is null")
            return

        print('Hello Timer!', self.tickCodeList)

        ## 获取实时tick数据
        try:
            df = ts.get_realtime_quotes(self.tickCodeList)
            #print(df)
            if df.empty:
                print("data is null")
            else:
            #DataForm格式数据, 数据格式转换为vnpy

                for rowIndex, item in enumerate(df.index):
                    code = df.iloc[rowIndex]['code']
                    #print(code)

                    if code not in self.tickDict:
                        tick = VtTickData()
                        tick.gatewayName = self.gatewayName

                        # 添加到字典中
                        self.tickDict[code] = tick
                    else:
                        tick = self.tickDict[code]

                    # tick数据，格式封装成vnpy格式
                    tick.symbol = code
                    tick.vtSymbol = code
                    tick.lastPrice = df.iloc[rowIndex]['bid']            # 最新成交价
                    tick.lastVolume = df.iloc[rowIndex]['b1_v']             # 最新成交量
                    tick.volume = df.iloc[rowIndex]['volume']                 # 今天总成交量
                    tick.name = df.iloc[rowIndex]['name']                 # 代码名称
                    #tick.openInterest = EMPTY_INT           # 持仓量
                    tick.time = df.iloc[rowIndex]['time']
                    tick.date = df.iloc[rowIndex]['date']
                    #tick.datetime = None                    # python的datetime时间对象

                    # 常规行情
                    tick.openPrice = df.iloc[rowIndex]['open']            # 今日开盘价
                    tick.highPrice = df.iloc[rowIndex]['high']            # 今日最高价
                    tick.lowPrice = df.iloc[rowIndex]['low']             # 今日最低价
                    tick.preClosePrice = df.iloc[rowIndex]['pre_close']

                    #tick.upperLimit = EMPTY_FLOAT           # 涨停价
                    #tick.lowerLimit = EMPTY_FLOAT           # 跌停价


                    # 五档行情
                    tick.bidPrice1 = df.iloc[rowIndex]['b1_p']
                    tick.bidPrice2 = df.iloc[rowIndex]['b2_p']
                    tick.bidPrice3 = df.iloc[rowIndex]['b3_p']
                    tick.bidPrice4 = df.iloc[rowIndex]['b4_p']
                    tick.bidPrice5 = df.iloc[rowIndex]['b5_p']

                    tick.askPrice1 = df.iloc[rowIndex]['a1_p']
                    tick.askPrice2 = df.iloc[rowIndex]['a2_p']
                    tick.askPrice3 = df.iloc[rowIndex]['a3_p']
                    tick.askPrice4 = df.iloc[rowIndex]['a4_p']
                    tick.askPrice5 = df.iloc[rowIndex]['a5_p']


                    tick.bidVolume1 = df.iloc[rowIndex]['b1_v']
                    tick.bidVolume2 = df.iloc[rowIndex]['b2_v']
                    tick.bidVolume3 = df.iloc[rowIndex]['b3_v']
                    tick.bidVolume4 = df.iloc[rowIndex]['b4_v']
                    tick.bidVolume5 = df.iloc[rowIndex]['b5_v']

                    tick.askVolume1 = df.iloc[rowIndex]['a1_v']
                    tick.askVolume2 = df.iloc[rowIndex]['a2_v']
                    tick.askVolume3 = df.iloc[rowIndex]['a3_v']
                    tick.askVolume4 = df.iloc[rowIndex]['a4_v']
                    tick.askVolume5 = df.iloc[rowIndex]['a5_v']


        except pymongo.errors.DuplicateKeyError:
            print("DuplicateKey")

        self.gateway.onTick(tick)

    #----------------------------------------------------------------------
    def onBaseStockDict(self):
        """获取有效的股票字典"""
        print('onBaseStockList!', self.stockDict)

        ## get_realtime_quotes
        try:
            df = ts.get_stock_basics()
            #print(df)
            if df.empty:
                print("data is null")
            else:
                #DataForm格式数据, 数据格式转换为vnpy
                for index, item in enumerate(df.index):
                    code = item
                    name = df.iloc[index]['name']
                    self.stockDict[code] = name
                    #print('stockDict:', code, name)


        except pymongo.errors.DuplicateKeyError:
            print("DuplicateKey")

        #记录数据库
        #self.gateway.onObjDict(self.stockDict)

    #----------------------------------------------------------------------
    def exit(self):
        """exit"""
        self.onStop()


    #----------------------------------------------------------------------
    """
    @function :save the data of basic report
    """
    def save_basic_report(self, client):
        '''保存今天的基本面数据'''

        #获取所有股票基本信息
        df = ts.get_stock_basics()
        collection = client.database.basic_report
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


    #----------------------------------------------------------------------
    """
    @function save the data of k
    @parameter db: database
    @parameter mytype: the type of k

    code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
    start：开始日期，格式YYYY-MM-DD
    end：结束日期，格式YYYY-MM-DD
    ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
    retry_count：当网络异常后重试次数，默认为3
    pause:重试时停顿秒数，默认为0

    """
    def getHistoryData(self, code, ktype='D', autype='qfq', start='', end=''):
        '''保存数据'''

        try:
            df = ts.get_k_data(code, ktype=mytype, autype=autype, start=start, end=end)
            if df.empty:
                print("null")
                return None
            else:
                return df

        except:
            print("BulkWriteError")
        return None


    #----------------------------------------------------------------------
    """
    @function save the data of k
    @parameter db: database
    @parameter mytype: the type of k
    当日分笔历史数据请调用get_today_ticks()接口
    历史分笔接口只能获取当前交易日之前的数据, get_tick_data()

    code：股票代码，即6位数字代码
    date：日期，格式YYYY-MM-DD
    retry_count : int, 默认3,如遇网络等问题重复执行的次数
    pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题

    """

    def getTodayTicks(self, code):
        '''当日分笔历史数据'''

        try:
            df = ts.get_today_ticks(code)
            if df.empty:
                print("df is empty")
                return None
            else:
                return df
        except:
            print("gateway getTodayTicks fail")

        return None

#----------------------------------------------------------------------
def test():

    #trade api
    wudituTrade = WudituTradeApi()
    #wudituTrade.webInit()
    #web.webInitLoaclPage()

    #data api
    wudituData = WudituDataApi()
    print('请登陆')
    try:
        while 1:

            num = input('输入测试流程： ')
            if num == '9':
                wudituTrade.exit()
                break

            # 检查是否处于登陆状态，如果没有登陆，需要重新登陆
            flag = wudituTrade.webCheckLogin()
            #print('webCheckLogin', flag)
            if flag == False:
                print('登陆失败，请重新登陆')
                continue

            # 测试流程
            if num == '1':
                #用户手工登陆，验证码无法自动识别
                #web.webLogin()
                pass
            elif num == '2':
                wudituTrade.setNormalBuyPage()
            elif num == '3':
                wudituTrade.setCreditBuyPage()
            elif num == '4':
                wudituTrade.setNormalSellPage()
            elif num == '5':
                wudituTrade.onBuy('002500', '11.00', '100')
            elif num == '6':
                wudituTrade.onSell('002500', '12.01', '100')

    except:
        print('except')
    finally:
        print('EXIT')
        wudituData.__del__()

if __name__ == '__main__':

    #test2()
    #test()

    client = MongoClient("localhost", 27017)
    api = TushareDataApi(None, client)
    api.save_basic_report(client)
    #web.webInit()



