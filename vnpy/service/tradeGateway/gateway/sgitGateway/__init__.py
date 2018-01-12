# encoding: UTF-8

from vnpy.service.language import vtConstant
from .sgitGateway import SgitGateway

gatewayClass = SgitGateway
gatewayName = 'SGIT'
gatewayDisplayName = '飞鼠'
gatewayType = vtConstant.GATEWAYTYPE_FUTURES
gatewayQryEnabled = True
