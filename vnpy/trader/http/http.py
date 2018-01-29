# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 17:17:05 2017

@author: chen
"""

# 重载sys模块，设置默认字符串编码方式为utf8
import sys
from imp import reload
reload(sys)

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


# 调试模式
#import tornado.autoreload

from vnpy.trader.tradeRiskCtrl import riskCtrl1
from vnpy.trader.http.routes.entry_index import routeHandler

from tornado.options import define, options
#巴拉巴拉import一大堆tornado的东西，反正都有用，原封不动即可
#define ("port", default=8080, help="run on the given port", type=int)
#定义监听的端口，随便挑个喜欢的数字吧
import tornado.ioloop
import tornado.web

from vnpy.trader.http.controller.task import TaskHandler
from vnpy.trader.http.controller.strategy import StrategyHandler
from vnpy.trader.http.controller.riskCtrl import RiskCtrlHandler
from vnpy.trader.http.controller.gateway import GatewayHandler
from vnpy.trader.http.controller.stock import StockHandler


########################################################################
class HttpHandler(object):
    """主引擎"""

    #----------------------------------------------------------------------
    def __init__(self, mainEngine):
        """Constructor"""

        self.mainEngine = mainEngine
        self.routeHandler=[
            (r"/task/(\w+)", TaskHandler, dict(mainEngine=mainEngine)),
            (r"/riskctrl/(\w+)", RiskCtrlHandler, dict(mainEngine=mainEngine)),
            (r"/strategy/(\w+)", StrategyHandler, dict(mainEngine=mainEngine)),
            (r"/gateway/(\w+)", GatewayHandler, dict(mainEngine=mainEngine)),
            (r"/stock/(\w+)", StockHandler, dict(mainEngine=mainEngine))
            ];


        #print('start http', self.routeHandler)

        tornado.options.parse_command_line()
        app = tornado.web.Application(handlers=self.routeHandler, debug = True)
        #app.listen(8080)

        self.http_server = tornado.httpserver.HTTPServer(app)
        self.http_server.listen(9000)

        print('start http loop, listen 9000')
        self.loop = tornado.ioloop.IOLoop.instance()
        self.loop.start()


    #----------------------------------------------------------------------
    def __del__(self):
        """Disconstructor"""
        self.http_server.stop()
        self.loop.stop()
        tornado.ioloop.IOLoop.clear_instance()

    #----------------------------------------------------------------------
    def start(self):
        pass


    #----------------------------------------------------------------------
    def stop(self):
        pass




#----------------------------------------------------------------------
if __name__ == "__main__":
    HttpHandler()
