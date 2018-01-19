# -*- coding: utf-8 -*-

from mongoengine import connect
from pymongo import MongoClient
from vnpy.trader.db import dbTask, dbTradeObject

################################################################################################################################################
class DBHandler(object):
    """主引擎"""

    #----------------------------------------------------------------------
    def __init__(self, mainEngine):
        """Constructor"""


        self.mainEngine = mainEngine

        connect('database', host='localhost', port=27017)
        print('connect to database db')

        self.client = MongoClient("localhost", 27017)
        self.taskHandler = dbTask.DBTaskHandler
        self.tradeObjHandler = dbTradeObject.TradeObjectHandler


    #----------------------------------------------------------------------
    def start(self):
        pass