# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 17:17:05 2017

@author: chen
"""
import tornado.ioloop
import tornado.web

from vnpy.service.http.controller.task import TaskHandler
from vnpy.service.http.controller.strategy import StrategyHandler
########################################################################
routeHandler=[
            (r"/task/(\w+)", TaskHandler),
            (r"/task/(\w+)/(\w+)", TaskHandler),
            (r"/firstInput/(\w+)", StrategyHandler)
];


