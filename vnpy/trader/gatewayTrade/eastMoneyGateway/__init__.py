# encoding: UTF-8

from vnpy.trader.language import vtConstant
from .eastMoney import EastMoneyTradeApi
from vnpy.trader.gatewayMarket.tushare.tushare import TushareDataApi

gatewayTradeClass = EastMoneyTradeApi
#配置行情接口
gatewayMarketClass =TushareDataApi
gatewayName = 'EastMoneyGateway'
gatewayDisplayName = '东方财富接口'
gatewayType = vtConstant.GATEWAYTYPE_EQUITY
gatewayQryEnabled = True

