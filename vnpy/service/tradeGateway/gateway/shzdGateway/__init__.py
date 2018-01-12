# encoding: UTF-8

from vnpy.service.language import vtConstant
from .shzdGateway import ShzdGateway

gatewayClass = ShzdGateway
gatewayName = 'SHZD'
gatewayDisplayName = '直达'
gatewayType = vtConstant.GATEWAYTYPE_INTERNATIONAL
gatewayQryEnabled = True

