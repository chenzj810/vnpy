# encoding: UTF-8

'''
本文件包含了STUB引擎中的策略开发用模板，开发策略时需要继承StubTemplate类。
'''

from vnpy.service.event import Event
from vnpy.service.language.vtConstant import *
from vnpy.service.main.vtObject import *
from vnpy.service.event.vtEvent import *


'''
本文件中包含了STUB模块中用到的一些基础设置、类和常量等。
'''



# 常量定义
# STUB引擎中涉及到的交易方向类型
STUBORDER_BUY = '买开'
STUBORDER_SELL = '卖平'
STUBORDER_SHORT = '卖开'
STUBORDER_COVER = '买平'

# 本地停止单状态
STOPORDER_WAITING = '等待中'
STOPORDER_CANCELLED = '已撤销'
STOPORDER_TRIGGERED = '已触发'

# 本地停止单前缀
STOPORDERPREFIX = 'StubStopOrder.'

# 数据库名称
SETTING_DB_NAME = 'VnTrader_Setting_Db'
POSITION_DB_NAME = 'VnTrader_Position_Db'

TICK_DB_NAME = 'VnTrader_Tick_Db'
DAILY_DB_NAME = 'VnTrader_Daily_Db'
MINUTE_DB_NAME = 'VnTrader_1Min_Db'

# 引擎类型，用于区分当前策略的运行环境
ENGINETYPE_BACKTESTING = 'backtesting'  # 回测
ENGINETYPE_TRADING = 'trading'          # 实盘

# STUB引擎中涉及的数据类定义
from vnpy.service.language.vtConstant import EMPTY_UNICODE, EMPTY_STRING, EMPTY_FLOAT, EMPTY_INT

########################################################################
class StrategyTemplate(object):
    """策略模板"""

    # 策略类的名称和作者
    className = 'StubTemplate'
    author = EMPTY_UNICODE

    # MongoDB数据库的名称，K线数据库默认为1分钟
    tickDbName = TICK_DB_NAME
    barDbName = MINUTE_DB_NAME

    # 策略的基本参数
    name = EMPTY_UNICODE           # 策略实例名称
    vtSymbol = EMPTY_STRING        # 交易的合约vt系统代码
    productClass = EMPTY_STRING    # 产品类型（只有IB接口需要）
    currency = EMPTY_STRING        # 货币（只有IB接口需要）

    # 策略的基本变量，由引擎管理
    inited = False                 # 是否进行了初始化
    trading = False                # 是否启动交易，由引擎管理
    pos = 0                        # 持仓情况
    myTask = ''

    # 参数列表，保存了参数的名称
    paramList = ['name',
                 'className',
                 'author',
                 'vtSymbol']

    # 变量列表，保存了变量的名称
    varList = ['inited',
               'trading',
               'pos']

    #----------------------------------------------------------------------
    def __init__(self, mainEngine, name=None):
        """Constructor"""
        self.mainEngine = mainEngine
        self.eventEngine = mainEngine.eventEngine
        self.historyData = mainEngine.historyData
        self.name = name


        # 设置策略的参数
        '''
        if setting:
            d = self.__dict__
            for key in self.paramList:
                if key in setting:
                    d[key] = setting[key]
        '''


    #----------------------------------------------------------------------
    def onInit(self, gateway, code):
        """初始化策略（必须由用户继承实现）"""
        self.gateway = gateway
        self.code = code

    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        raise NotImplementedError

    #----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        raise NotImplementedError

    #----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        raise NotImplementedError

    #----------------------------------------------------------------------
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        raise NotImplementedError

    #----------------------------------------------------------------------
    def onTrade(self, trade):
        """收到成交推送（必须由用户继承实现）"""
        raise NotImplementedError

    #----------------------------------------------------------------------
    def onBar(self, bar):
        """收到Bar推送（必须由用户继承实现）"""
        raise NotImplementedError

    #----------------------------------------------------------------------
    def onbuy(self, stockCode, price, amount):
        """买开"""
        #发送 交易任务
        if self.gateway:
            #gateway.onBuy(stockCode, price, amount)
            print('发送买单, code:%s, price:%s, amount:%s', stockCode, price, amount)
            self.writeLog('发送买单, code:%s, price:%s, amount:%s', stockCode, price, amount)
        #return self.sendOrder(STUBORDER_BUY, price, volume, stop)

    #----------------------------------------------------------------------
    def onSell(self, stockCode, price, amount):
        """卖平"""
         #发送 交易任务

        if self.gateway:
            #gateway.onSell(stockCode, price, amount)
            print('发送卖单, code:%s, price:%s, amount:%s', stockCode, price, amount)
            self.writeLog('发送卖单, code:%s, price:%s, amount:%s', stockCode, price, amount)




    #----------------------------------------------------------------------
    def insertTick(self, tick):
        """向数据库中插入tick数据"""
        self.mainEngine.insertData(self.tickDbName, self.vtSymbol, tick)

    #----------------------------------------------------------------------
    def insertBar(self, bar):
        """向数据库中插入bar数据"""
        self.mainEngine.insertData(self.barDbName, self.vtSymbol, bar)


    #----------------------------------------------------------------------
    def loadBar(self, code, ktype, days):
        """从数据库中读取Bar数据，startDate是datetime对象"""
        #startDate = self.today - timedelta(days)

        #d = {'datetime':{'$gte':startDate}}
        df = self.historyData.historyDataQuery(code, ktype)

        l = []
        for d in df:
            bar = VtBarData()
            bar.__dict__ = d
            l.append(bar)
        return l

    #----------------------------------------------------------------------
    def loadTick(self, dbName, collectionName, days):
        """从数据库中读取Tick数据，startDate是datetime对象"""
        startDate = self.today - timedelta(days)

        d = {'datetime':{'$gte':startDate}}
        tickData = self.historyData.historyDataQuery(code, ktype, d)

        l = []
        for d in tickData:
            tick = VtTickData()
            tick.__dict__ = d
            l.append(tick)
        return l


    #----------------------------------------------------------------------
    def writeLog(self, content):
        """快速发出模块日志事件"""
        log = VtLogData()
        log.logContent = content
        event = Event(type_=EVENT_LOG)
        event.dict_['data'] = log
        self.eventEngine.put(event)

    #----------------------------------------------------------------------
    def putEvent(self):
        """发出策略状态变化事件"""
        """触发策略状态变化事件（通常用于通知GUI更新）"""
        event = Event(EVENT_STRATEGY+self.name)
        self.eventEngine.put(event)

    #----------------------------------------------------------------------
    def getEngineType(self):
        """查询当前运行的环境"""
        return self.eventEngine.engineType

