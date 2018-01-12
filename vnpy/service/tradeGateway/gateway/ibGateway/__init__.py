# encoding: UTF-8

from vnpy.service.language import vtConstant
from .ibGateway import IbGateway

gatewayClass = IbGateway
gatewayName = 'IB'
gatewayDisplayName = gatewayName
gatewayType = vtConstant.GATEWAYTYPE_INTERNATIONAL
gatewayQryEnabled = False