# encoding: UTF-8


import json
import os


from vnpy.trader.config.vtGlobal import globalSetting
from vnpy.trader.language import text
from vnpy.trader.main.vtFunction import getTempPath



########################################################################
class HistoryDataTemplate(object):
    """历史数据引擎"""

    settingFileName = 'config_setting.json'
    path = os.path.abspath(os.path.dirname(__file__))
    settingFileName = os.path.join(path, settingFileName)


    #----------------------------------------------------------------------
    def __init__(self, mainEngine):
        """Constructor"""
        self.eventEngine = mainEngine.eventEngine

        #self.eventEngine.register(EVENT_TICK, self.onTickRecod)


   #----------------------------------------------------------------------
    def historyDataConnect(self):
        """历史数据打开（必须由用户继承实现）"""
        raise NotImplementedError

   #----------------------------------------------------------------------
    def historyDataOpen(self, code, ktype):
        """历史数据打开（必须由用户继承实现）"""
        raise NotImplementedError


   #----------------------------------------------------------------------
    def historyDataClose(self, code, ktype):
        """历史数据关闭（必须由用户继承实现）"""
        raise NotImplementedError

    #----------------------------------------------------------------------
    def historyDataInsert(self, code, ktype, df):
        """插入数据历史数据，df是具体数据, 格式是dataForm（必须由用户继承实现）"""
        raise NotImplementedError


    #----------------------------------------------------------------------
    def historyDataQuery(self, code, ktype):
        """读取数据（必须由用户继承实现）"""
        raise NotImplementedError


    #----------------------------------------------------------------------
    def historyDataUpdate(self, code, ktype, df):
        """更新数据（必须由用户继承实现）"""
        raise NotImplementedError



    #----------------------------------------------------------------------
    def writeLog(self, content):
        """快速发出日志事件"""
        log = VtLogData()
        log.logContent = content
        event = Event(type_=EVENT_LOG)
        event.dict_['data'] = log
        self.eventEngine.put(event)




'''
    #----------------------------------------------------------------------
    def saveSetting(self):
        """保存策略配置"""
        with open(self.settingFileName, 'w') as f:
            l = []

            for strategy in list(self.strategyDict.values()):
                setting = {}
                for param in strategy.paramList:
                    setting[param] = strategy.__getattribute__(param)
                l.append(setting)

            jsonL = json.dumps(l, indent=4)
            f.write(jsonL)


    #----------------------------------------------------------------------
    def loadSetting(self):
        """读取策略配置"""
        with open(self.settingFileName) as f:
            setting = json.load(f)

            if setting['historyDataSaveMode'] == 'file':
                from .historyDataFile import historyDataFile
                self.getInst()
            f.close()

'''


########################################################################
class HistoryDataManager(object):
    """历史数据管理"""



    #----------------------------------------------------------------------
    def __init__(self, mainEngine):
        """Constructor"""
        self.historyData = mainEngine.historyData
        self.eventEngine = mainEngine.eventEngine

        #self.eventEngine.register(EVENT_TICK, self.onTickRecod)