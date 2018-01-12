# encoding: UTF-8

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

########################################################################
class TaskHandler(tornado.web.RequestHandler):
    """handler"""

    #----------------------------------------------------------------------
    def get(self, *args, **kwargs):

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

        self.finish()

    #----------------------------------------------------------------------
    def post(self, *args, **kwargs):

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

        self.finish()


    #----------------------------------------------------------------------
    def __list(self, *args, **kwargs):
        print('args:', str(args), str(kwargs))
        self.write(', friendly user!')

    #----------------------------------------------------------------------
    def __add(self, *args, **kwargs):
        print('args:', str(args), str(kwargs))
        self.write(', friendly user!')

    #----------------------------------------------------------------------
    def __del(self, *args, **kwargs):
        print('args:', str(args), str(kwargs))
        self.write(', friendly user!')

    #----------------------------------------------------------------------
    def __start(self, *args, **kwargs):
        print('args:', str(args), str(kwargs))
        self.write(', friendly user!')

    #----------------------------------------------------------------------
    def __stop(self, *args, **kwargs):
        print('args:', str(args), str(kwargs))
        self.write(', friendly user!')
