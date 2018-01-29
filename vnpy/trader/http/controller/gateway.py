# encoding: UTF-8


import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json


########################################################################
class GatewayHandler(tornado.web.RequestHandler):
    """主引擎"""

    #----------------------------------------------------------------------
    def initialize(self, mainEngine):
        self.mainEngine = mainEngine


    #----------------------------------------------------------------------
    def get(self,  *args, **kwargs):

        print(self.request.method, self.request.uri, 'args:', str(args))
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

        print(self.request.method, self.request.uri, 'args:', str(args))
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
    def __list(self, *args, **kwargs):
        mylist = []
        for i, item in enumerate(self.mainEngine.getAllGatewayList()):
            mylist.append(item['gatewayDisplayName'])

        self.write({"ret_code": 0, "ret_msg": "FAILED", "extra":mylist})

    #----------------------------------------------------------------------
    def __add(self, *args, **kwargs):
        print(self.request.body_arguments)

        self.write('hello, __add')

    #----------------------------------------------------------------------
    def __del(self, *args, **kwargs):
        self.write('hello, __del')

    #----------------------------------------------------------------------
    def __start(self, *args, **kwargs):
        self.write('hello, __start')

    #----------------------------------------------------------------------
    def __stop(self, *args, **kwargs):
        self.write('hello, __stop')