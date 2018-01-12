# encoding: UTF-8

from vnpy.service.language import vtConstant
from .femasGateway import FemasGateway

gatewayClass = FemasGateway
gatewayName = 'FEMAS'
gatewayDisplayName = '飞马'
gatewayType = vtConstant.GATEWAYTYPE_FUTURES
gatewayQryEnabled = True
