# encoding: UTF-8

from vnpy.trader.language import vtConstant
from .eastMoney import EastMoneyTradeApi

gatewayClass = EastMoneyTradeApi
gatewayName = 'EastMoneyGateway'
gatewayDisplayName = '东方财富接口'
gatewayType = vtConstant.GATEWAYTYPE_EQUITY
gatewayQryEnabled = True

