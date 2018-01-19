# encoding: UTF-8

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from vnpy.trader.config.vtGlobal import globalSetting
from vnpy.trader.language import text
from vnpy.trader.main.vtFunction import getTempPath
from vnpy.trader.dbHistory.vtHistoryDataManager import HistoryDataTemplate



########################################################################
class HistoryDataDB(HistoryDataTemplate):
    """数据引擎"""
    contractFileName = 'ContractData.vt'
    contractFilePath = getTempPath(contractFileName)

    #----------------------------------------------------------------------
    def __init__(self, mainEngine):
        """Constructor"""
        self.eventEngine = mainEngine.eventEngine

        # MongoDB数据库相关
        self.dbClient = None    # MongoDB客户端对象

        self.dbName = 'mydb'    # MongoDB客户端对象
        self.collectionName = 'myConllection'


        # 注册事件监听
        self.registerEvent()



    #----------------------------------------------------------------------
    def __dbInsert(self, dbName, collectionName, d):
        """向MongoDB中插入数据，d是具体数据"""

        if self.dbClient:
            db = self.dbClient[dbName]
            collection = db[collectionName]
            collection.insert_one(d)
        else:
            self.writeLog(text.DATA_INSERT_FAILED)


    #----------------------------------------------------------------------
    def __dbQuery(self, dbName, collectionName, d):
        """从MongoDB中读取数据，d是查询要求，返回的是数据库查询的指针"""

        if self.dbClient:
            db = self.dbClient[dbName]
            collection = db[collectionName]
            cursor = collection.find(d)
            if cursor:
                return list(cursor)
            else:
                return []
        else:
            self.writeLog(text.DATA_QUERY_FAILED)
            return []

    #----------------------------------------------------------------------
    def __dbUpdate(self, dbName, collectionName, d, flt, upsert=False):
        """向MongoDB中更新数据，d是具体数据，flt是过滤条件，upsert代表若无是否要插入"""

        if self.dbClient:
            db = self.dbClient[dbName]
            collection = db[collectionName]
            collection.replace_one(flt, d, upsert)
        else:
            self.writeLog(text.DATA_UPDATE_FAILED)

    #----------------------------------------------------------------------
    def dbLogging(self, event):
        """向MongoDB中插入日志"""

        log = event.dict_['data']
        d = {
            'content': log.logContent,
            'time': log.logTime,
            'gateway': log.gatewayName
        }
        self.dbInsert(LOG_DB_NAME, self.todayDate, d)


   #----------------------------------------------------------------------
    def dbConnect(self):
        """连接MongoDB数据库"""

        print(__name__, self.__doc__)

        if not self.dbClient:
            # 读取MongoDB的设置
            try:
                # 设置MongoDB操作的超时时间为0.5秒
                self.dbClient = MongoClient(globalSetting['mongoHost'], globalSetting['mongoPort'], connectTimeoutMS=500)

                # 调用server_info查询服务器状态，防止服务器异常并未连接成功
                self.dbClient.server_info()

                self.writeLog(text.DATABASE_CONNECTING_COMPLETED)

                # 如果启动日志记录，则注册日志事件监听函数
                if globalSetting['mongoLogging']:
                    self.eventEngine.register(EVENT_LOG, self.dbLogging)

            except ConnectionFailure:
                self.writeLog(text.DATABASE_CONNECTING_FAILED)

    #----------------------------------------------------------------------
    def dbInsert(self, df):
        """向MongoDB中插入数据，df是具体数据, 格式是dataForm"""
        self.__dbInsert(self.dbName, self.collectionName, df)


    #----------------------------------------------------------------------
    def dbQuery(self, dbName, collectionName, df):
        """从MongoDB中读取数据，d是查询要求，返回的是数据库查询的指针"""
        self.__dbQuery(self.dbName, self.collectionName, df)


    #----------------------------------------------------------------------
    def dbUpdate(self, dbName, df):
        """向MongoDB中更新数据，d是具体数据，flt是过滤条件，upsert代表若无是否要插入"""
        self.__dbUpdate(self.dbName, self.collectionName, df)



    #----------------------------------------------------------------------
    def writeLog(self, content):
        """快速发出日志事件"""
        log = VtLogData()
        log.logContent = content
        event = Event(type_=EVENT_LOG)
        event.dict_['data'] = log
        self.eventEngine.put(event)


    #----------------------------------------------------------------------
    def registerEvent(self):
        """注册事件监听"""
        #self.eventEngine.register(EVENT_ORDER, self.updateOrder)



