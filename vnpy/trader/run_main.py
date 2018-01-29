
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:40:25 2017

@author: chen
在vnpy基础上修改
"""

# encoding: UTF-8

# 重载sys模块，设置默认字符串编码方式为utf8
import sys
from imp import reload
reload(sys)
#sys.setdefaultencoding('utf8')

# vn.trader模块
from vnpy.trader.event.eventEngine import EventEngine
from vnpy.trader.main.vtEngine import MainEngine


# 加载底层接口
from vnpy.trader.gatewayTrade import eastMoneyGateway
from vnpy.trader.gatewayMarket import tushare


#from vnpy.trader import riskManager
#from vnpy.trader import strategyManager
from vnpy.trader.tradeStrategy import strategyAtrRsi
from vnpy.trader.tradeStrategy import strategyDualThrust
from vnpy.trader.tradeStrategy import strategyMacdShake
from vnpy.trader.tradeRiskCtrl import riskCtrl1


from vnpy.trader.db.models import DBHandler
from vnpy.trader.http.http import HttpHandler


#----------------------------------------------------------------------
def main():
    """主程序入口"""

    print("main start")
    # 创建事件引擎
    ee = EventEngine()

    # 创建主引擎
    me = MainEngine(ee)

    me.DB = DBHandler(me)

    # 添加交易接口， 包括行情数据接口和交易接口两部分
    print("添加gateway接口, addGatewayClass")
    me.addGatewayClass(eastMoneyGateway)


    # 添加上层应用, 应用管理
    #me.addApp(strategyManager)

    print("添加上层应用, addRiskCtrlClass")
    me.addRiskCtrlClass(riskCtrl1)

    print("添加上层应用, addStrategyClass")
    me.addStrategyClass(strategyDualThrust)
    me.addStrategyClass(strategyAtrRsi)
    me.addStrategyClass(strategyMacdShake)


    HttpHandler(me)

    try:
        me.exit()
        sys.exit(0)
    except:
        print('GoodBye!')
        pass


if __name__ == '__main__':
    main()