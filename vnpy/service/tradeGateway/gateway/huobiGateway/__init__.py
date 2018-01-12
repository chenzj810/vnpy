# encoding: UTF-8

from vnpy.service.language import vtConstant
from .huobiGateway import HuobiGateway

gatewayClass = HuobiGateway
gatewayName = 'HUOBI'
gatewayDisplayName = '火币'
gatewayType = vtConstant.GATEWAYTYPE_BTC
gatewayQryEnabled = True

