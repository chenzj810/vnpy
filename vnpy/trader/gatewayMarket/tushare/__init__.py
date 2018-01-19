# encoding: UTF-8

from vnpy.trader.language import vtConstant
from .tushare import TushareDataApi

gatewayClass = TushareDataApi
gatewayName = 'TushareGateway'
gatewayDisplayName = 'Tushare接口'
gatewayType = vtConstant.GATEWAYTYPE_EQUITY
gatewayQryEnabled = True

