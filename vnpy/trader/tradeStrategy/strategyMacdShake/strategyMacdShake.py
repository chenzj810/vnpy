# encoding: UTF-8

"""
DualThrust交易策略
"""


import datetime
import time
from vnpy.trader.event.vtEvent import *
from vnpy.trader.main.vtObject import VtBarData, VtTickData
from vnpy.trader.language.vtConstant import EMPTY_STRING
from vnpy.trader.tradeStrategy.vtStrategyManager import StrategyTemplate
import talib as ta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd





########################################################################
class MacdShakeStrategy(StrategyTemplate):
    """DualThrust交易策略"""
    className = 'MacdShakeStrategy'
    author = 'chenzejun'



    #----------------------------------------------------------------------
    def __init__(self, mainEngine, name):
        """Constructor"""
        super(MacdShakeStrategy, self).__init__(mainEngine, name)

        ## 收市时间
        self.exitTime = '15:55:00'
        self.barList = []
        self.name = name
        self.barMinute = None
        self.bar = None


        self.dateList=[]
        self.openList=[]
        self.closeList=[]
        self.highList=[]
        self.lowList=[]
        self.volumeList=[]


    #----------------------------------------------------------------------
    def onInit(self, gateway, code):
        """初始化策略（必须由用户继承实现）"""
        self.gateway = gateway
        self.code = code
        self.writeLog('strategy onInit')

        # 同步时间长，显示任务需要等待时间太长
        # self.onTickSync(code)


        # 注册tick接收
        self.eventEngine.register(EVENT_TICK + code, self.onTick)


    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        print('启动策略')
        self.writeLog(self.name + '策略启动')
        self.onTickHistorySync(self.code)
        #self.eventEngine.register(EVENT_TICK, self.onTick)

    #----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        print('停止策略')
        self.writeLog(self.name + '策略停止')
        self.eventEngine.unregister(EVENT_TICK + self.code, self.onTick)


    #----------------------------------------------------------------------
    '''
              time  price pchange  change  volume   amount type
    0     13:42:45  12.01    0.00    0.01       1     1201   买盘
    1     13:42:42  12.00   -0.08   -0.01       7     8400   卖盘
    2     13:42:36  12.01    0.00    0.01       1     1201   买盘
    3     13:42:33  12.00   -0.08   -0.01      20    24000   卖盘
    4     13:42:21  12.01    0.00    0.01       8     9608   买盘
    5     13:42:12  12.00   -0.08   -0.01       4     4800   卖盘
    6     13:42:03  12.01    0.00    0.01      29    34829   买盘
    '''
    def onTickHistorySync(self, code):
        """tick数据同步"""

        # gateway 获取数据
        if self.gateway is None:
            self.writeLog('gateway is None')
            return


        tickMinute = 0  # 初始化


        df = self.gateway.getTodayTicks(code)
        if df is None:
            self.writeLog('onTickSync, getTodayTicks is None')
            return

        print('onTickHistorySync, df:', df.shape, "code:", code)

        # 计算列位置，通过iat 位置取单元格的值，速度快
        column_price = list(df.columns).index('price')
        column_time = list(df.columns).index('time')
        column_volume = list(df.columns).index('volume')


        # 转换数据, 需要使用reversed 进行反向遍历
        tick = VtTickData()
        for n, rowIndex in enumerate(reversed(df.index)):
            #格式：2017-09-14 13:42:45

            tick.time = df.iat[rowIndex, column_time]    #格式：13:42
            tick.date = str(datetime.date.today()) + ' ' + tick.time   #格式：2017-09-14 13:42:45
            tick.lastPrice = df.iat[rowIndex, column_price]
            tick.volume = df.iat[rowIndex, column_volume]

            self.tickDataProcess(tick)



        '''
        # 转换数据, 需要使用reversed 进行反向遍历
        for n, rowIndex in enumerate(reversed(df.index)):
            #新的1分钟
            struct_time = time.strptime(df.iat[rowIndex, column_time], "%H:%M:%S")
            tickMinute = struct_time.tm_min     # 更新当前的分钟

            if tickMinute != self.barMinute:
                #首次不能添加
                if self.bar:
                    # add to list
                    self.dateList.append(bar.date)
                    self.openList.append(bar.open)
                    self.closeList.append(bar.close)
                    self.highList.append(bar.high)
                    self.lowList.append(bar.low)
                    self.volumeList.append(bar.volume)


                    # add to empty dataform
                    mydf.loc[n] = [bar.date, bar.open, bar.close, bar.high, bar.low, bar.volume, code]
                    #print('srowIndex', n, rowIndex)

                    # add to barlist
                    self.onMin1Bar(bar)


                # new start
                # new  bar data
                bar = VtBarData()
                #bar.symbol = df.iat[rowIndex]['code']
                bar.open = df.iat[rowIndex, column_price]
                bar.high = df.iat[rowIndex, column_price]
                bar.low = df.iat[rowIndex, column_price]
                bar.close = df.iat[rowIndex, column_price]
                bar.volume = 0

                #datetime.date.today()    #格式：2017-09-14
                #df.iat[rowIndex]['time']    #格式：13:42:45
                bar.time = df.iat[rowIndex, column_time]    #格式：13:42
                bar.date = str(datetime.date.today()) + ' ' + bar.time   #格式：2017-09-14 13:42:45

                self.barMinute = tickMinute     # 更新当前的分钟
                #print('self.barMinute', self.barMinute)
                self.bar = bar                  # 这种写法为了减少一层访问，加快速度
            else:                               # 否则继续累加新的K线
                bar = self.bar                  # 写法同样为了加快速度

                bar.high = max(bar.high, df.iat[rowIndex, column_price])
                bar.low = min(bar.low, df.iat[rowIndex, column_price])
                bar.close = df.iat[rowIndex, column_price]
                bar.volume = bar.volume + df.iat[rowIndex, column_volume]

        '''

        # 生成空的pandas表
        mydf = pd.DataFrame(columns=('date', 'open', 'close', 'high', 'low', 'volume', 'code'))
        #mydf = pd.DataFrame({'date':'', 'open':'', 'close':'', 'high':'', 'low':'', 'volume':'', 'code':''})
        for n, bar in enumerate(self.barList):
            mydf.loc[n] = [bar.date, bar.open, bar.close, bar.high, bar.low, bar.volume, code]
        print('mydf:', mydf.columns)
        #print(mydf)

        # 更新历史数据， 存数据库或文件
        self.historyData.historyDataUpdate(code, '1', mydf)



        # 载入历史数据，并采用回放计算的方式初始化策略数值
        #initData = self.loadBar(code, '1', 1)
        #for bar in initData:
        #self.onMin1Bar(bar)

        #self.putEvent()

    #----------------------------------------------------------------------
    def onTick(self, event):
        """收到行情TICK推送）"""
        # 这个函数可以注册到tick事件上

        tick = event.dict_['data']

        print('onTick, time:', tick.time)
        self.tickDataProcess(tick)


    #----------------------------------------------------------------------
    def tickDataProcess(self, tick):
        """收到行情TICK推送, 历史tick"""


        print('tickDataProcess, time:', tick.time)
        struct_time = time.strptime(tick.time, "%H:%M:%S")
        tickMinute = struct_time.tm_min

        bar = self.bar
        if tickMinute != self.barMinute:
            if bar:
                # add to list
                self.dateList.append(bar.date)
                self.openList.append(bar.open)
                self.closeList.append(bar.close)
                self.highList.append(bar.high)
                self.lowList.append(bar.low)
                self.volumeList.append(bar.volume)

                self.onMin1Bar(self.bar)
            else:
                # the first
                # new  bar data
                self.bar = VtBarData()
                bar = self.bar

            #bar.vtSymbol = tick.vtSymbol
            #bar.symbol = tick.symbol
            #bar.exchange = tick.exchange

            bar.open = tick.lastPrice
            bar.high = tick.lastPrice
            bar.low = tick.lastPrice
            bar.close = tick.lastPrice
            bar.volume = 0

            bar.date = tick.date
            bar.time = tick.time
            bar.datetime = tick.datetime    # K线的时间设为第一个Tick的时间

            self.barMinute = tickMinute     # 更新当前的分钟
        else:                               # 否则继续累加新的K线

            bar.high = max(bar.high, tick.lastPrice)
            bar.low = min(bar.low, tick.lastPrice)
            bar.close = tick.lastPrice
            bar.volume = bar.volume + int(tick.volume)


    #----------------------------------------------------------------------
    """
    @function 1分k线处理
    @parameter bar: bar
    """
    def onMin1Bar(self, bar):
        """收到Bar推送"""
        # 撤销之前发出的尚未成交的委托（包括限价单和停止单）
        '''
        for orderID in self.orderList:
            self.cancelOrder(orderID)
        self.orderList = []
        '''

        # 计算指标数值
        self.barList.append(bar)
        print('onMin1Bar, barList count:', len(self.barList), bar.date)


        if len(self.barList) <= 2:
            return
        else:
            #self.barList.pop(0)
            pass


        # 是否在交易时间
        #print(self.exitTime)
        if self.isTradeTime(bar.time):
            # print('closeList:', self.closeList)
            try:
                dif, dea, macd = ta.MACD(np.array(self.closeList), fastperiod=12, slowperiod=26, signalperiod=9)
                #if, dea, macd = self.myMACD(np.array(self.closeList), fastperiod=12, slowperiod=26, signalperiod=9)
            except:
                print('except')
                return

            print('dif:', len(dif), 'dea:', len(dea), 'macd:', len(macd))
            print('dif:', dif[len(dif)-1], 'dea:', dea[len(dea)-1], 'macd:', macd[len(macd)-1])


        # 1. 计算周期

        # 2. 双背离


        # 收盘平仓
        else:
            if self.pos > 0:
                self.onSell(bar.close * 0.99, abs(self.pos))
            elif self.pos < 0:
                self.cover(bar.close * 1.01, abs(self.pos))

        # 发出状态更新事件
        #self.putEvent()

    #----------------------------------------------------------------------
    def compare_time(self, l_time,start_t,end_t):
        """时间比较函数"""

        s_time = time.mktime(time.strptime(start_t,'%Y%m%d%H%M')) # get the seconds for specify date
        e_time = time.mktime(time.strptime(end_t,'%Y%m%d%H%M'))
        log_time = time.mktime(time.strptime(l_time,'%Y-%m-%d %H:%M:%S'))


        if (float(log_time) >= float(s_time)) and (float(log_time) <= float(e_time)):
            return True

        return False

    #----------------------------------------------------------------------
    def isTradeTime(self, date):
        """判断是否交易时间"""
        return True

    #----------------------------------------------------------------------
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        pass

    #----------------------------------------------------------------------
    def onTrade(self, trade):
        # 发出状态更新事件
        self.putEvent()

    #----------------------------------------------------------------------
    def myMACD(price, fastperiod=12, slowperiod=26, signalperiod=9):
        ewma12 = pd.ewma(price,span=fastperiod)
        ewma60 = pd.ewma(price,span=slowperiod)
        dif = ewma12-ewma60
        dea = pd.ewma(dif,span=signalperiod)
        macd = (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
        return dif,dea,macd