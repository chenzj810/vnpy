# encoding: UTF-8


import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

########################################################################
class StrategyHandler(tornado.web.RequestHandler):
    """主引擎"""

    #----------------------------------------------------------------------
    def __init__(self, eventEngine):
        """Constructor"""



    #----------------------------------------------------------------------
    def get(self, id=None):

        self.write(', friendly user!')

    #----------------------------------------------------------------------
    def post(self, id=None):
        self.write(', friendly user!')


