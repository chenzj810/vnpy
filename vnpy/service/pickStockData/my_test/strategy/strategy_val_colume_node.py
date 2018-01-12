# encoding: UTF-8

"""
DualThrust交易策略
采用量柱选股策略
"""

from datetime import time

from vnpy.service.main.vtObject import VtBarData
from vnpy.service.language.vtConstant import EMPTY_STRING
from vnpy.service.app.ctaStrategy.ctaTemplate import CtaTemplate


########################################################################
class ValColumeStrategy(object):
    """量柱选股策略"""
    className = 'DualThrustStrategy'
    author = u'用Python的交易员'

    # 策略参数
    fastK = 0.9     # 快速EMA参数
    slowK = 0.1     # 慢速EMA参数
    initDays = 10   # 初始化数据所用的天数

    # 策略变量
    bar = None
    barMinute = EMPTY_STRING

    fastMa = []             # 快速EMA均线数组
    fastMa0 = EMPTY_FLOAT   # 当前最新的快速EMA
    fastMa1 = EMPTY_FLOAT   # 上一根的快速EMA

    slowMa = []             # 与上面相同
    slowMa0 = EMPTY_FLOAT
    slowMa1 = EMPTY_FLOAT

    # 参数列表，保存了参数的名称
    paramList = ['name',
                 'className',
                 'author',
                 'vtSymbol',
                 'fastK',
                 'slowK']

    # 变量列表，保存了变量的名称
    varList = ['inited',
               'trading',
               'pos',
               'fastMa0',
               'fastMa1',
               'slowMa0',
               'slowMa1']

    #----------------------------------------------------------------------
    def __init__(self, ctaEngine, setting):
        """Constructor"""

        #super(EmaDemoStrategy, self).__init__(ctaEngine, setting)

        # 注意策略类中的可变对象属性（通常是list和dict等），在策略初始化时需要重新创建，
        # 否则会出现多个策略实例之间数据共享的情况，有可能导致潜在的策略逻辑错误风险，
        # 策略类中的这些可变对象属性可以选择不写，全都放在__init__下面，写主要是为了阅读
        # 策略时方便（更多是个编程习惯的选择）
        self.fastMa = []
        self.slowMa = []
        self.dbClient = MongoClient("localhost", 27017)


    #----------------------------------------------------------------------
    def onInit(self):
        """初始化策略（必须由用户继承实现）"""
        #self.writeCtaLog(u'双EMA演示策略初始化')

        initData = self.loadBar(self.initDays)
        for bar in initData:
            self.onBar(bar)

        self.putEvent()

    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        self.writeCtaLog(u'%s策略启动' %self.name)
        self.putEvent()

    #----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        self.writeCtaLog(u'%s策略停止' %self.name)
        self.putEvent()

    #----------------------------------------------------------------------
    def loadDataInDatabase(bar):
        """停止策略（必须由用户继承实现）"""
        dbClient = MongoClient("localhost", 27017)

        #根据今天的日k 线数据进行选股
        today = datetime.date.today() #获得今天的日期

        #collection 数据集合
        collection_basic = client.basic_report.records
        collection_result = client.select_result.basic_env
        my_db = client.day


    #----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        # 计算K线
        tickMinute = tick.datetime.minute

        if tickMinute != self.barMinute:
            if self.bar:
                self.onBar(self.bar)

            bar = VtBarData()
            bar.vtSymbol = tick.vtSymbol
            bar.symbol = tick.symbol
            bar.exchange = tick.exchange

            bar.open = tick.lastPrice
            bar.high = tick.lastPrice
            bar.low = tick.lastPrice
            bar.close = tick.lastPrice

            bar.date = tick.date
            bar.time = tick.time
            bar.datetime = tick.datetime    # K线的时间设为第一个Tick的时间

            self.bar = bar                  # 这种写法为了减少一层访问，加快速度
            self.barMinute = tickMinute     # 更新当前的分钟
        else:                               # 否则继续累加新的K线
            bar = self.bar                  # 写法同样为了加快速度

            bar.high = max(bar.high, tick.lastPrice)
            bar.low = min(bar.low, tick.lastPrice)
            bar.close = tick.lastPrice

    #----------------------------------------------------------------------
    def onBar(self, bar):
        """收到Bar推送（必须由用户继承实现）"""
        # 撤销之前发出的尚未成交的委托（包括限价单和停止单）
        for orderID in self.orderList:
            self.cancelOrder(orderID)
        self.orderList = []

        # 计算指标数值
        self.barList.append(bar)

        if len(self.barList) <= 2:
            return
        else:
            self.barList.pop(0)
        lastBar = self.barList[-2]

        # 新的一天
        if lastBar.datetime.date() != bar.datetime.date():
            # 如果已经初始化
            if self.dayHigh:
                self.range = self.dayHigh - self.dayLow
                self.longEntry = bar.open + self.k1 * self.range
                self.shortEntry = bar.open - self.k2 * self.range

            self.dayOpen = bar.open
            self.dayHigh = bar.high
            self.dayLow = bar.low

            self.longEntered = False
            self.shortEntered = False
        else:
            self.dayHigh = max(self.dayHigh, bar.high)
            self.dayLow = min(self.dayLow, bar.low)

        # 尚未到收盘
        if not self.range:
            return

        if bar.datetime.time() < self.exitTime:
            if self.pos == 0:
                if bar.close > self.dayOpen:
                    if not self.longEntered:
                        vtOrderID = self.buy(self.longEntry, self.fixedSize, stop=True)
                        self.orderList.append(vtOrderID)
                else:
                    if not self.shortEntered:
                        vtOrderID = self.short(self.shortEntry, self.fixedSize, stop=True)
                        self.orderList.append(vtOrderID)

            # 持有多头仓位
            elif self.pos > 0:
                self.longEntered = True

                # 多头止损单
                vtOrderID = self.sell(self.shortEntry, self.fixedSize, stop=True)
                self.orderList.append(vtOrderID)

                # 空头开仓单
                if not self.shortEntered:
                    vtOrderID = self.short(self.shortEntry, self.fixedSize, stop=True)
                    self.orderList.append(vtOrderID)

            # 持有空头仓位
            elif self.pos < 0:
                self.shortEntered = True

                # 空头止损单
                vtOrderID = self.cover(self.longEntry, self.fixedSize, stop=True)
                self.orderList.append(vtOrderID)

                # 多头开仓单
                if not self.longEntered:
                    vtOrderID = self.buy(self.longEntry, self.fixedSize, stop=True)
                    self.orderList.append(vtOrderID)

        # 收盘平仓
        else:
            if self.pos > 0:
                vtOrderID = self.sell(bar.close * 0.99, abs(self.pos))
                self.orderList.append(vtOrderID)
            elif self.pos < 0:
                vtOrderID = self.cover(bar.close * 1.01, abs(self.pos))
                self.orderList.append(vtOrderID)

        # 发出状态更新事件
        self.putEvent()

    #----------------------------------------------------------------------
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        pass

    #----------------------------------------------------------------------
    def onTrade(self, trade):
        # 发出状态更新事件
        self.putEvent()
