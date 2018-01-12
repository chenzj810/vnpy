# encoding: UTF-8

from vnpy.service.language import vtConstant
from .ksotpGateway import KsotpGateway

gatewayClass = KsotpGateway
gatewayName = 'KSOTP'
gatewayDisplayName = '金仕达期权'
gatewayType = vtConstant.GATEWAYTYPE_EQUITY
gatewayQryEnabled = True

