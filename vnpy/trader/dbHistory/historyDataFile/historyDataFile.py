# encoding: UTF-8


from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from vnpy.trader.event import Event
from vnpy.trader.config.vtGlobal import globalSetting
from vnpy.trader.event.vtEvent import *
from vnpy.trader.gatewayTrade.vtGateway import *
from vnpy.trader.language import text
from vnpy.trader.main.vtFunction import getTempPath
from vnpy.trader.dbHistory.vtHistoryDataManager import HistoryDataTemplate

import pandas as pd
import numpy as np


########################################################################
class HistoryDataFile(HistoryDataTemplate):
    """文件引擎"""

    #----------------------------------------------------------------------
    def __init__(self, mainEngine):
        """Constructor"""

        super(HistoryDataFile, self).__init__(mainEngine)

        # file数据库相关
        self.file = None    # MongoDB客户端对象
        self.filePath = self.path    # 使用类变量


        self.eventEngine.register(EVENT_TICK, self.onTickRecod)

    #----------------------------------------------------------------------
    def getFileName(self, code, ktype):
        """向file中插入数据，df是具体数据, 格式是dataForm"""

        if code[0] == '6':
            exchange = 'sh'
        else:
            exchange = 'sz'


        if ktype == 'D':
            fileName = self.filePath + exchange + '/day/' + exchange + code + '.csv'
        elif ktype == 'W':
            fileName = self.filePath + exchange + '/week/' + exchange + code + '.csv'
        elif ktype == 'M':
            fileName = self.filePath + exchange + '/month/' + exchange + code + '.csv'
        elif ktype == '1':
            fileName = self.filePath + exchange + '/min1/' + exchange + code + '.csv'
        elif ktype == '5':
            fileName = self.filePath + exchange + '/min5/' + exchange + code + '.csv'
        elif ktype == '15':
            fileName = self.filePath + exchange + '/min15/' + exchange + code + '.csv'
        elif ktype == '30':
            fileName = self.filePath + exchange + '/min30/' + exchange + code + '.csv'
        elif ktype == '60':
            fileName = self.filePath + exchange + '/min60/' + exchange + code + '.csv'
        else:
            return None

        return fileName

    '''
    df=ts.get_k_data('002500', ktype='5')
                     date   open  close   high    low   volume    code
    0    2017-08-31 14:55  12.19  12.21  12.21  12.18  17141.0  002500
    1    2017-08-31 15:00  12.21  12.22  12.22  12.20  12261.0  002500
    2    2017-09-01 09:35  12.28  12.24  12.33  12.20  30416.0  002500
    3    2017-09-01 09:40  12.24  12.27  12.29  12.22  23025.0  002500
    4    2017-09-01 09:45  12.27  12.31  12.31  12.25  24376.0  002500
    '''
    #----------------------------------------------------------------------
    def historyDataInsert(self, code, ktype, df):
        """向file中插入数据，df是具体数据, 格式是dataForm"""

        fileName = self.getFileName(code, ktype)

        if fileName != None:
            #直接保存
            df.to_csv(fileName)


    #----------------------------------------------------------------------
    def historyDataQuery(self, code, ktype):
        """从file中读取数据，d是查询要求，返回的是数据库查询的指针"""
        fileName = self.getFileName(code, ktype)

        if fileName != None:
            #直接保存
            df = pd.read_csv(fileName)
            print(df)
            return df


    #----------------------------------------------------------------------
    def historyDataUpdate(self, code, ktype, df):
        """向file中更新数据，df是具体数据"""

        fileName = self.getFileName(code, ktype)

        if fileName != None:
            #直接保存
            df.to_csv( )




    #----------------------------------------------------------------------
    def writeLog(self, content):
        """快速发出日志事件"""
        log = VtLogData()
        log.logContent = content
        event = Event(type_=EVENT_LOG)
        event.dict_['data'] = log
        self.eventEngine.put(event)


    #----------------------------------------------------------------------
    def onTickRecod(self, event):
        """onTickRecod"""

        tick = event.dict_['data']

        print('historyDataUpdate, tick received, code:', tick.symbol)
        #historyDataUpdate(tick.symbol, '1', df)
