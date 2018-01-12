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
from vnpy.event import EventEngine
from vnpy.trader.vtEngine import MainEngine
from vnpy.trader.uiQt import qApp
from vnpy.trader.uiMainWindow import MainWindow


# 加载底层接口
from vnpy.trader.gateway import stubNullGateway

# 加载上层应用
from vnpy.trader.app import riskManager
from vnpy.trader.app import stubStrategy
from vnpy.trader.app import dataRecorder


#----------------------------------------------------------------------
def main():
    """主程序入口"""
    # 创建事件引擎
    ee = EventEngine()

    # 创建主引擎
    me = MainEngine(ee)

    # 添加交易接口
    me.addGateway(stubNullGateway)

    # 添加上层应用
    me.addApp(riskManager)

    print("1111111")
    me.addApp(stubStrategy)

    me.addApp(dataRecorder)
    print("22222")

    # 创建主窗口
    mw = MainWindow(me, ee)
    mw.showMaximized()

    # 在主线程中启动Qt事件循环
    qApp.exec_()
    sys.exit(0)


if __name__ == '__main__':
    main()