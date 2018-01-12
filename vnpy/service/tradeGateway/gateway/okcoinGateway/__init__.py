# encoding: UTF-8

from vnpy.service.language import vtConstant
from .okcoinGateway import OkcoinGateway

gatewayClass = OkcoinGateway
gatewayName = 'OKCOIN'
gatewayDisplayName = '币行'
gatewayType = vtConstant.GATEWAYTYPE_BTC
gatewayQryEnabled = True

