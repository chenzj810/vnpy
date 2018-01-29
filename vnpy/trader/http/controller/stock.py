# encoding: UTF-8

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json

########################################################################
class StockHandler(tornado.web.RequestHandler):
    """handler"""

    def initialize(self, mainEngine):
        self.mainEngine = mainEngine
        self.dbClient = mainEngine.DB.client
        print('me:', mainEngine)

    #----------------------------------------------------------------------
    def get(self, *args, **kwargs):

        print(self.request.method, self.request.uri, 'args:', str(args))
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Content-Type","application/json")

        if args[0] == 'list':
            self.__list(args, kwargs)
        elif args[0] == 'name':
            self.__name(args, kwargs)
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
        elif args[0] == 'name':
            self.__name(args, kwargs)
        else:
            self.write({"ret_code": -1, "ret_msg": "FAILED", "extra":"url invalid"})

        self.finish()


    #----------------------------------------------------------------------
    def __list(self, *args, **kwargs):
        mylist = []

         # 创建迭代器对象, 遍历列表
        list_name = self.dbClient.database.basic_report.find()
        for item in list_name:
            #print(item)
            code = item['code']
            name = item['name']
            #print(code, name)
            mylist.append({code:name})

        #print(mylist)
        self.write({"ret_code": 0, "ret_msg":"FAILED", "extra":mylist})

    #----------------------------------------------------------------------
    def __name(self, *args, **kwargs):
        #print(self.request.body)

        try:
            stock_code = self.get_argument('stock_code')
            item = self.dbClient.database.basic_report.find_one({"code":stock_code})

            #print('stock_code', stock_code, item['name'])
            self.write({"ret_code": 0, "ret_msg":"SUCCESS", "extra":item['name']})
        except:
            self.write({"ret_code": -1, "ret_msg":"FAILED", "extra":'not found'})





    """
    function
    @param db_data: 数据库
    @param collection_base: 基本面数据集合
    @param date: 日期
    @param collection_result: 结果输出数据集合
    """

    def select_by_basic_db(self, db_data, collection_base, date, collection_result):
        '''根据日线数据和基本面数据选股'''


        # 创建迭代器对象, 遍历列表
        list_name = collection_base.find()
        for item in list_name:
            #创建股票代码命名的集合
            #print(item)

            #print(item['code'])
            code = item['code']
            #print(code)


            collection_code = db_data[code]
            #print(collection_code)


            #周六，周日时，节假日时，往前找有数据的天进行选股
            for i in range(0, -10, -1):
                delta = datetime.timedelta(days=i)
                my_date = str(date + delta)
                #print(my_date)

                 #今天的记录收盘价
                today_record = collection_code.find_one({'date':my_date})
                if today_record is not None:
                    #print(today_record)

                    #基本面3倍选股
                    select_by_basic_policy(collection_result, item, today_record, BASE_OF_MAX_WEIGHT)
                    break;

            #退出
        return

    """
    @function:select_by_basic
    @param void:
    @return void:
    @rtype void:
    """
    def select_by_basic(self):
        '''今天的k数据进行选股'''

        client = self.dbClient

        #根据今天的日k 线数据进行选股
        today = datetime.date.today() #获得今天的日期

        #collection 数据集合
        collection_basic = client.basic_report.records
        collection_result = client.select_result.basic_env
        my_db = client.day
        #print(collection)


        #删除上次选股的全部记录
        collection_result.remove()

        #重新选股
        select_by_basic_db(my_db, collection_basic, today, collection_result)
        return

    """
    @function:select_by_basic
    @param void:
    @return void:
    @rtype void:
    """
    def select_by_basic(self):
        '''今天的k数据进行选股'''

        client = self.dbClient

        #根据今天的日k 线数据进行选股
        today = datetime.date.today() #获得今天的日期

        #collection 数据集合
        collection_basic = client.basic_report.records
        collection_result = client.select_result.basic_env
        my_db = client.day
        #print(collection)


        #删除上次选股的全部记录
        collection_result.remove()

        #重新选股
        select_by_basic_db(my_db, collection_basic, today, collection_result)
        return