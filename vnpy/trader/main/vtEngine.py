# encoding: UTF-8

import os
import shelve
from collections import OrderedDict
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from vnpy.trader.event import Event
from vnpy.trader.config.vtGlobal import globalSetting
from vnpy.trader.event.vtEvent import *
from vnpy.trader.gatewayTrade.vtGateway import *
from vnpy.trader.language import text
from vnpy.trader.main.vtFunction import getTempPath
from vnpy.trader.dbHistory.historyDataFile.historyDataFile import HistoryDataFile
from vnpy.trader.dbHistory.historyDataDB.historyDataDB import HistoryDataDB

########################################################################
class MainEngine(object):
    """主引擎"""

    #----------------------------------------------------------------------
    def __init__(self, eventEngine):
        """Constructor"""
        # 记录今日日期
        self.todayDate = datetime.now().strftime('%Y%m%d')

        # 绑定事件引擎
        self.eventEngine = eventEngine
        self.eventEngine.start()

        # 创建数据引擎
        self.dataEngine = DataEngine(self.eventEngine)


        # 创建文件引擎，直接保存文件，比数据库方便
        #self.fileEngine = FileEngine(self)

        # 历史数据保存方式, 根据配置文件实例化
        if globalSetting['historyDataSaveMode'] == 'file':
            self.historyData = HistoryDataFile(self)
        elif globalSetting['historyDataSaveMode'] == 'db':
            self.historyData = HistoryDataDB(self)
        else:
            self.historyData = None

        # 历史数据字典，key:code, data:
        self.historyDataDict = OrderedDict()
        self.historyDataList = []




        self.DB = None

        '''
        # 行情接口gateway接口类型管理，字典，key：gatewayName
        self.marketGatewayDict = OrderedDict()
        self.marketGatewayList = []

        # 交易接口gateway接口类型管理，字典，key：gatewayName
        self.tradeGatewayDict = OrderedDict()
        self.tradeGatewayList = []
        '''

        # 交易接口gateway接口类型管理，字典，key：gatewayName
        self.gatewayDict = OrderedDict()
        self.gatewayList = []

        # begin chenzejun
        # 风控类型管理，字典，key：riskCtrlName
        self.riskCtrlDict = OrderedDict()
        self.riskCtrlDetailList = []

        # 策略类型管理，字典，key：strategyName
        self.strategyDict = OrderedDict()
        self.strategyDetailList = []


        # 应用模块实例
        #self.appDict = OrderedDict()
        self.appDetailList = []


        # 有效的标的列表，股票信息模块, 股票代码，名称
        # 现在是股票列表，chenzejun
        self.validObjectDict = {}


        # 任务实例字典, 创建的任务，key：code+strategyName+riskCtrlName+gatewayName
        # 一个交易任务包括，策略，风控，底层接口，可以多实例运行
        self.taskInstanceDict = {}

        # end chenzejun

        # 风控引擎实例（特殊独立对象）
        self.rmEngine = None


    #----------------------------------------------------------------------
    def addObjDict(self, event):
        """添加标的字典到主引擎，做有效性检查，联想等"""

        # 保存应用信息
        print('\n收到标的字典更新:', event.type_)
        data = event.dict_['data']
        self.validObjectDict = data


    #----------------------------------------------------------------------
    def objectIsValid(self, code):
        """检查标的是否有效"""

        # 检查标的
        return code in self.validObjectDict

    #----------------------------------------------------------------------
    def objectGetValue(self, code):
        """获取标的的值"""

        # 检查标的
        return self.validObjectDict[code]


    #----------------------------------------------------------------------
    def addApp(self, appModule):
        """添加上层应用"""
        #appName = appModule.appName

        # 创建应用实例
        #self.appDict[appName] = appModule.appEngine(self, self.eventEngine)

        # 保存应用信息
        d = {
            'appName': appModule.appName,
            'appDisplayName': appModule.appDisplayName,
            #'appWidget': appModule.appWidget,
            'appIco': appModule.appIco
        }

        print('addApp', appModule.appName, d['appIco'])
        self.appDetailList.append(d)


    # begin chenzejun
    #----------------------------------------------------------------------
    def addGatewayClass(self, gatewayModule):
        """添加底层接口"""

        gatewayName = gatewayModule.gatewayName

        #生成gateway的实例
        appTradeInst = gatewayModule.gatewayTradeClass(self.eventEngine, self.DB.client)
        appyMarketInst = gatewayModule.gatewayMarketClass(self.eventEngine, self.DB.client)

        # 保存接口详细信息
        d = {
            'gatewayName': gatewayModule.gatewayName,
            'gatewayDisplayName': gatewayModule.gatewayDisplayName,
            'gatewayType': gatewayModule.gatewayType,
            'gatewayMarketClass': appyMarketInst,
            'gatewayTradeClass' : appTradeInst
        }
        self.gatewayDict[gatewayName] = d
        self.gatewayList.append(d)


    '''
    #----------------------------------------------------------------------
    def addMarketGatewayClass(self, gatewayModule):
        """添加底层接口"""

        gatewayName = gatewayModule.gatewayName

        #生成gateway的实例
        appInst = gatewayModule.gatewayClass(self.eventEngine, self.DB.client)

        # 保存接口详细信息
        d = {
            'gatewayName': gatewayModule.gatewayName,
            'gatewayDisplayName': gatewayModule.gatewayDisplayName,
            'gatewayType': gatewayModule.gatewayType,
            'gatewayInstance' : appInst
        }
        self.marketGatewayDict[gatewayName] = d
        self.marketGatewayList.append(d)
    '''

    #----------------------------------------------------------------------
    def addStrategyClass(self, appModule):
        """添加策略上层应用"""
        appName = appModule.appName

        # 创建应用实例
        #self.strategyDict[appName] = appModule.appEngine(self, '')

        # 保存应用信息
        d = {
            'appName': appModule.appName,
            'appDisplayName': appModule.appDisplayName,
            'appEngine': appModule.appEngine,
            #'appWidget': appModule.appWidget,
            #'appIco': appModule.appIco
        }

        print('add StrategyType:', d['appDisplayName'], appName)
        self.strategyDict[appName] = d
        self.strategyDetailList.append(d)

    #----------------------------------------------------------------------
    def addRiskCtrlClass(self, appModule):
        """添加风控上层应用"""
        appName = appModule.appName

        # 保存应用信息
        d = {
            'appName': appModule.appName,
            'appDisplayName': appModule.appDisplayName,
            'appEngine': appModule.appEngine,
            #'appWidget': appModule.appWidget,
            #'appIco': appModule.appIco
        }

        # 创建应用实例
        self.riskCtrlDict[appName] = d
        self.riskCtrlDetailList.append(d)




    #----------------------------------------------------------------------
    def getAllStrategyList(self):
        """查询引擎中所有上层应用的信息"""
        return self.strategyDetailList

    #----------------------------------------------------------------------
    def getAllRiskCtrlList(self):
        """查询引擎中所有上层应用的信息"""
        return self.riskCtrlDetailList

    #----------------------------------------------------------------------
    def getAllGatewayList(self):
        """查询引擎中所有上层应用的信息"""
        return self.gatewayList


    #----------------------------------------------------------------------
    def newStrategy(self, appName):
        """获取策略类接口, 支持多实例"""

        appClass = self.strategyDict[appName]['appEngine']
        return appClass(self, appName)

    #----------------------------------------------------------------------
    def newRiskCtrl(self, appName):
        """获取风控类接口, 支持多实例"""

        appClass = self.riskCtrlDict[appName]['appEngine']
        return appClass(self, appName)

    #----------------------------------------------------------------------
    def newGateway(self, appName):
        """获取Gateway类接口， 唯一实例"""
        # gateway 只支持单实例运行，这里是统一是有new命名
        # 唯一实例，add class时创建， 这里返回已创建的实例
        return self.tradeGatewayDict[appName]['gatewayInstance']

    def getStrategyName(self, displayName):
        """获取策略类接口"""

        for k, v in self.strategyDict.items():
            print('getStrategyName:', k, len(self.strategyDict))
            if v['appDisplayName'] == displayName:
                return v['appName']

        return None


    #----------------------------------------------------------------------
    def getRiskCtrlName(self, displayName):
        """获取风控类接口"""

        for (k,v) in  self.riskCtrlDict.items():
            if v['appDisplayName'] == displayName:
                return v['appName']

        return None


    #----------------------------------------------------------------------
    def getGatewayName(self, displayName):
        """获取Gateway类接口"""

        for (k,v) in  self.tradeGatewayDict.items():
            if v['gatewayDisplayName'] == displayName:
                return v['gatewayName']

        return None

    #----------------------------------------------------------------------
    def addTaskInstance(self, task):
        """添加任务实例"""

        # 创建应用实例
        key = task.strategyName + task.riskCtrlName + task.gatewayName + task.symbol
        self.taskInstanceDict[key] = task

    #----------------------------------------------------------------------
    def newTask(self, task):
        """获取任务实例接口"""

        if task.strategyName is None:
            self.writeLog('策略实例不存在，无法运行')
            return -1

        if task.riskCtrlName is None:
            self.writeLog('风控实例不存在，无法运行')
            return -2

        if task.gatewayName is None:
            self.writeLog('底层实例不存在，无法运行')
            return -3

        #key：strategyName+riskCtrlName+gatewayName+symbol
        key = task.strategyName + task.riskCtrlName + task.gatewayName + task.symbol
        if key in self.taskInstanceDict:
            return 1
        else:
            # 启动数据接口
            # 单实例运行，每个任务对应一个code进去
            task.gateway = self.newGateway(task.gatewayName)
            if task.gateway:
                task.gateway.onInit(task.symbol)


            # 创建应用实例
            task.strategy = self.newStrategy(task.strategyName)
            if task.strategy:
                task.strategy.onInit(task.gateway, task.symbol)


            #获取app engine
            # 启动风控， 多实例运行
            task.riskCtrl = self.newRiskCtrl(task.riskCtrlName)
            if task.riskCtrl:
                task.riskCtrl.onInit()


            # 添加任务实例
            self.addTaskInstance(task)

            '''
            # start task
            if task.gateway:
                task.gateway.onStart()
            if task.strategy:
                task.strategy.onStart()
            if task.riskCtrl:
                task.riskCtrl.onStart()
            '''
            return 0


    #----------------------------------------------------------------------
    def delTask(self, key):
        """获取任务实例接口"""
        if key in self.taskInstanceDict:
            task = self.taskInstanceDict.pop(key)
            task.gateway.onUpdate('del', task.symbol)
            task.strategy.onStop()
            task.riskCtrl.onStop()
        else:
            self.writeLog('task is not exist')
            return None

    #----------------------------------------------------------------------
    def startTask(self, key):
        """开始已停止的任务"""
        if key in self.taskInstanceDict:
            task = self.taskInstanceDict[key]

            # 更新任务列表，启动gateway
            task.gateway.onUpdate('add', task.symbol)
            task.gateway.onStart()
            task.strategy.onStart()
            task.riskCtrl.onStart()
            return task
        else:
            self.writeLog('task is not exist')
            return None

    #----------------------------------------------------------------------
    def stopTask(self, key):
        """停止任务"""
        if key in self.taskInstanceDict:
            task = self.taskInstanceDict[key]
            task.gateway.onUpdate('del', task.symbol)
            return task
        else:
            self.writeLog('task is not exist')
            return None

    #----------------------------------------------------------------------
    def connect(self, gatewayName):
        """连接特定名称的接口"""
        gateway = self.getGateway(gatewayName)

        if gateway:
            gateway.connect()

            # 接口连接后自动执行数据库连接的任务
            self.dbEngine.dbConnect()

    #----------------------------------------------------------------------
    def subscribe(self, subscribeReq, gatewayName):
        """订阅特定接口的行情"""
        gateway = self.getGateway(gatewayName)

        if gateway:
            gateway.subscribe(subscribeReq)

    #----------------------------------------------------------------------
    def sendOrder(self, orderReq, gatewayName):
        """对特定接口发单"""
        # 如果创建了风控引擎，且风控检查失败则不发单
        if self.rmEngine and not self.rmEngine.checkRisk(orderReq):
            return ''

        gateway = self.getGateway(gatewayName)

        if gateway:
            return gateway.sendOrder(orderReq)
        else:
            return ''

    #----------------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq, gatewayName):
        """对特定接口撤单"""
        gateway = self.getGateway(gatewayName)

        if gateway:
            gateway.cancelOrder(cancelOrderReq)

    #----------------------------------------------------------------------
    def qryAccount(self, gatewayName):
        """查询特定接口的账户"""
        gateway = self.getGateway(gatewayName)

        if gateway:
            gateway.qryAccount()

    #----------------------------------------------------------------------
    def qryPosition(self, gatewayName):
        """查询特定接口的持仓"""
        gateway = self.getGateway(gatewayName)

        if gateway:
            gateway.qryPosition()

    #----------------------------------------------------------------------
    def exit(self):
        """退出程序前调用，保证正常退出"""

        # 安全关闭所有接口
        for task in list(self.taskInstanceDict.values()):
            if task.strategy is not None:
                task.strategy.onStop()

            if task.riskCtrl is not None:
                task.riskCtrl.onStop()

            if task.gateway is not None:
                task.gateway.close()

        # 停止事件引擎
        self.eventEngine.stop()

        # 停止上层应用引擎
        # begin chenzejun
        '''
        for appEngine in list(self.appDict.values()):
            appEngine.stop()
        '''
        # end chenzejun


        # 保存数据引擎里的合约数据到硬盘
        self.dataEngine.saveContracts()

    #----------------------------------------------------------------------
    def writeLog(self, content):
        """快速发出日志事件"""
        log = VtLogData()
        log.logContent = content
        event = Event(type_=EVENT_LOG)
        event.dict_['data'] = log
        self.eventEngine.put(event)


    #----------------------------------------------------------------------
    def getContract(self, vtSymbol):
        """查询合约"""
        return self.dataEngine.getContract(vtSymbol)

    #----------------------------------------------------------------------
    def getAllContracts(self):
        """查询所有合约（返回列表）"""
        return self.dataEngine.getAllContracts()

    #----------------------------------------------------------------------
    def getOrder(self, vtOrderID):
        """查询委托"""
        return self.dataEngine.getOrder(vtOrderID)

    #----------------------------------------------------------------------
    def getAllWorkingOrders(self):
        """查询所有的活跃的委托（返回列表）"""
        return self.dataEngine.getAllWorkingOrders()

    #----------------------------------------------------------------------
    def getAllGatewayDetails(self):
        """查询引擎中所有底层接口的信息"""
        return self.tradeGatewayList

    #----------------------------------------------------------------------
    def getAllAppDetails(self):
        """查询引擎中所有上层应用的信息"""
        # begin chenzejun
        return self.appDetailList
        # end chenzejun

########################################################################
class DataEngine(object):
    """数据引擎"""
    contractFileName = 'ContractData.vt'
    contractFilePath = getTempPath(contractFileName)

    #----------------------------------------------------------------------
    def __init__(self, eventEngine):
        """Constructor"""
        self.eventEngine = eventEngine

        # 保存合约详细信息的字典
        self.contractDict = {}

        # 保存委托数据的字典
        self.orderDict = {}

        # 保存活动委托数据的字典（即可撤销）
        self.workingOrderDict = {}

        # 读取保存在硬盘的合约数据
        self.loadContracts()

        # 注册事件监听
        self.registerEvent()

    #----------------------------------------------------------------------
    def updateContract(self, event):
        """更新合约数据"""
        contract = event.dict_['data']
        self.contractDict[contract.vtSymbol] = contract
        self.contractDict[contract.symbol] = contract       # 使用常规代码（不包括交易所）可能导致重复

    #----------------------------------------------------------------------
    def getContract(self, vtSymbol):
        """查询合约对象"""
        try:
            return self.contractDict[vtSymbol]
        except KeyError:
            return None

    #----------------------------------------------------------------------
    def getAllContracts(self):
        """查询所有合约对象（返回列表）"""
        return list(self.contractDict.values())

    #----------------------------------------------------------------------
    def saveContracts(self):
        """保存所有合约对象到硬盘"""
        f = shelve.open(self.contractFilePath)
        f['data'] = self.contractDict
        f.close()

    #----------------------------------------------------------------------
    def loadContracts(self):
        """从硬盘读取合约对象"""
        f = shelve.open(self.contractFilePath)
        if 'data' in f:
            d = f['data']
            for key, value in list(d.items()):
                self.contractDict[key] = value
        f.close()

    #----------------------------------------------------------------------
    def updateOrder(self, event):
        """更新委托数据"""
        order = event.dict_['data']
        self.orderDict[order.vtOrderID] = order

        # 如果订单的状态是全部成交或者撤销，则需要从workingOrderDict中移除
        if order.status == STATUS_ALLTRADED or order.status == STATUS_CANCELLED:
            if order.vtOrderID in self.workingOrderDict:
                del self.workingOrderDict[order.vtOrderID]
        # 否则则更新字典中的数据
        else:
            self.workingOrderDict[order.vtOrderID] = order

    #----------------------------------------------------------------------
    def getOrder(self, vtOrderID):
        """查询委托"""
        try:
            return self.orderDict[vtOrderID]
        except KeyError:
            return None

    #----------------------------------------------------------------------
    def getAllWorkingOrders(self):
        """查询所有活动委托（返回列表）"""
        return list(self.workingOrderDict.values())

    #----------------------------------------------------------------------
    def registerEvent(self):
        """注册事件监听"""
        self.eventEngine.register(EVENT_CONTRACT, self.updateContract)
        #self.eventEngine.register(EVENT_ORDER, self.updateOrder)



