# encoding: UTF-8

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
from vnpy.trader.language.vtConstant import EMPTY_UNICODE, EMPTY_STRING, EMPTY_FLOAT, EMPTY_INT


########################################################################
class StopOrder(object):
    """本地停止单"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.vtSymbol = EMPTY_STRING
        self.orderType = EMPTY_UNICODE
        self.direction = EMPTY_UNICODE
        self.offset = EMPTY_UNICODE
        self.price = EMPTY_FLOAT
        self.volume = EMPTY_INT
        
        self.strategy = None             # 下停止单的策略对象
        self.stopOrderID = EMPTY_STRING  # 停止单的本地编号 
        self.status = EMPTY_STRING       # 停止单状态