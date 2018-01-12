# encoding: UTF-8

from vnpy.service.language import vtConstant
from .stubNullGateway import stubNullGateway

gatewayClass = stubNullGateway
gatewayName = 'NULLSTUB'
gatewayDisplayName = '空桩Gateway'
gatewayType = vtConstant.GATEWAYTYPE_EQUITY
gatewayQryEnabled = True

