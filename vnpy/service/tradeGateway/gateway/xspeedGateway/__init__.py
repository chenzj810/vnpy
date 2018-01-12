# encoding: UTF-8

from vnpy.service.language import vtConstant
from .xspeedGateway import XspeedGateway

gatewayClass = XspeedGateway
gatewayName = 'XSPEED'
gatewayDisplayName = '飞创'
gatewayType = vtConstant.GATEWAYTYPE_FUTURES
gatewayQryEnabled = True