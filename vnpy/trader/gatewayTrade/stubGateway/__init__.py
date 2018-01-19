# encoding: UTF-8

from vnpy.trader.language import vtConstant
from .stubGateway import StubGateway

gatewayClass = StubGateway
gatewayName = 'STUB'
gatewayDisplayName = '桩Gateway'
gatewayType = vtConstant.GATEWAYTYPE_BTC
gatewayQryEnabled = True

