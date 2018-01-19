# encoding: UTF-8

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from mongoengine import *
from bson import json_util

########################################################################
class TaskHandler(tornado.web.RequestHandler):
    """handler"""

    def initialize(self, mainEngine):
        self.mainEngine = mainEngine
        self.DB = mainEngine.DB

    #----------------------------------------------------------------------
    def get(self, *args, **kwargs):

        print(self.request.headers.get("Content-Type"), 'args:', str(args))

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Content-Type","application/json")


        if args[0] == 'list':
            self.__list(args, kwargs)
        elif args[0] == 'add':
            self.__add(args, kwargs)
        elif args[0] == 'del':
            self.__del(args, kwargs)
        elif args[0] == 'start':
            self.__start(args, kwargs)
        elif args[0] == 'stop':
            self.__stop(args, kwargs)
        else:
            self.write({"ret_code": -1, "ret_msg": "FAILED", "extra":"url invalid"})

        self.finish()

    #----------------------------------------------------------------------
    def post(self, *args, **kwargs):

        #print(self.request.headers.get("Content-Type"), 'args:', str(args))
        print(self.request.method, 'args:', str(args))

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Content-Type","application/json")

        if args[0] == 'list':
            self.__list(args, kwargs)
        elif args[0] == 'add':
            self.__add(args, kwargs)
        elif args[0] == 'del':
            self.__del(args, kwargs)
        elif args[0] == 'start':
            self.__start(args, kwargs)
        elif args[0] == 'stop':
            self.__stop(args, kwargs)
        else:
            self.write({"ret_code": -1, "ret_msg": "FAILED", "extra":"url invalid"})

        self.finish()

    #----------------------------------------------------------------------
    def options(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("X-Powered-By",' 3.2.1')
        #self.set_header("Content-Type", "application/json;charset=utf-8")

        self.finish()


    #----------------------------------------------------------------------
    def __list(self, *args, **kwargs):

        try:
            mylist = []

            #tlist = self.DB.taskHandler.objects().order_by('task_id')
            objects = self.DB.taskHandler.objects().order_by('task_id')
            #mylist = json_util.dumps(objects._collection_obj.find(objects._query))
            for item in objects:
                mydict = {
                        "task_id":item.task_id,
                        "stock_code":item.stock_code,
                        "stock_name":item.stock_name,
                        "obj_amount":item.obj_amount,

                        "strategy_name":item.strategy_name,
                        "riskctrl_name":item.riskctrl_name,
                        "market_gateway":item.market_gateway,
                        "trade_gateway":item.trade_gateway
                        }

                #print("stock_name:", item.stock_name, "trade_gateway:",item.trade_gateway)
                mylist.append(mydict)

            #tlist = self.DB.taskHandler.objects().order_by('task_id')
            #print(mylist)

            self.write({"ret_code": 0, "ret_msg":"SUCCESS", "extra":mylist})
        except:
            self.write({"ret_code": -1, "ret_msg":"FAILED", "extra":'exception'})

    #----------------------------------------------------------------------
    def __add(self, *args, **kwargs):


        task = self.DB.taskHandler()

        try:
            task.stock_code = self.get_argument('stock_code')
        except:
            task.stock_code = 'default'

        try:
            task.stock_name = self.get_argument('stock_name')
        except:
            task.stock_name = 'default'

        try:
            task.obj_amount = self.get_argument('obj_amount')
        except:
            task.obj_amount = 'default'

        try:
            task.strategy_name = self.get_argument('strategy_name')
        except:
            task.strategy_name = 'default'

        try:
            task.riskctrl_name = self.get_argument('riskctrl_name')
        except:
            task.riskctrl_name = 'default'

        try:
            task.market_gateway = self.get_argument('market_gateway')
        except:
            task.market_gateway = 'default'

        try:
            task.trade_gateway = self.get_argument('trade_gateway')
        except:
            task.trade_gateway = 'default'


        task.save()

        self.write({"ret_code": 0, "ret_msg":"SUCCESS", "extra":task.stock_code})

    #----------------------------------------------------------------------
    def __del(self, *args, **kwargs):
        try:
            task_id = self.get_argument('task_id')
            self.DB.taskHandler.objects.filter(task_id=task_id).delete()
            self.write({"ret_code": 0, "ret_msg":"SUCCESS", "extra":task_id})
        except:
            self.write({"ret_code": -1, "ret_msg":"FAILED", "extra":'exception'})

    #----------------------------------------------------------------------
    def __start(self, *args, **kwargs):
        try:
            task_id = self.get_argument('task_id')
            self.write({"ret_code": 0, "ret_msg":"SUCCESS", "extra":task_id})
        except:
            self.write({"ret_code": -1, "ret_msg":"FAILED", "extra":'exception'})



            # 启动数据接口
            # 单实例运行，每个任务对应一个code进去
            task.gateway = self.mainEngine.newGateway(task.gatewayName)
            if task.gateway:
                task.gateway.onInit(task.symbol)


            # 创建应用实例
            task.strategy = self.mainEngine.newStrategy(task.strategyName)
            if task.strategy:
                task.strategy.onInit(task.gateway, task.symbol)


            #获取app engine
            # 启动风控， 多实例运行
            task.riskCtrl = self.mainEngine.newRiskCtrl(task.riskCtrlName)
            if task.riskCtrl:
                task.riskCtrl.onInit()





    #----------------------------------------------------------------------
    def __stop(self, *args, **kwargs):
        self.write('hello, __stop')