# encoding: UTF-8

from vnpy.service.language import vtConstant
from .eastMoneyGateway import EastMoneyGateway

gatewayClass = EastMoneyGateway
gatewayName = 'EastMoneyGateway'
gatewayDisplayName = '东方财富接口'
gatewayType = vtConstant.GATEWAYTYPE_EQUITY
gatewayQryEnabled = True

