# encoding: UTF-8

'''
本文件中实现了风控引擎，用于提供一系列常用的风控功能：
1. 委托流控（单位时间内最大允许发出的委托数量）
2. 总成交限制（每日总成交数量限制）
3. 单笔委托的委托数量控制
'''

from vnpy.trader.event import Event
from vnpy.trader.language.vtConstant import *
from vnpy.trader.main.vtObject import *
from vnpy.trader.event.vtEvent import *

########################################################################
class RiskCtrlTemplate(object):
    """风控引擎"""

    name = '风控模块'

    #----------------------------------------------------------------------
    def __init__(self, mainEngine, name):
        """Constructor"""
        self.mainEngine = mainEngine
        self.eventEngine = mainEngine.eventEngine
        self.name = name

    #----------------------------------------------------------------------
    def onInit(self):
        """初始化策略（必须由用户继承实现）"""
        pass

    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        raise NotImplementedError

    #----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        raise NotImplementedError

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