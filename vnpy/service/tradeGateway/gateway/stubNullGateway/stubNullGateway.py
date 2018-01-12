# encoding: UTF-8

'''
vn.stub的gateway接入
'''



from vnpy.service.vtGateway import VtGateway
from vnpy.service.main.vtObject import VtLogData
#import VtGateway
#import VtLogData




########################################################################
class stubNullGateway(VtGateway):
    """空的桩接口"""

    #----------------------------------------------------------------------
    def __init__(self, eventEngine, gatewayName='STUB'):
        """Constructor"""
        super(stubNullGateway, self).__init__(eventEngine, gatewayName)

        self.market = 'cny'



    #----------------------------------------------------------------------
    def connect(self):
        """连接"""
        pass

    #----------------------------------------------------------------------
    def writeLog(self, content):
        """发出日志"""
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = content
        self.onLog(log)

    #----------------------------------------------------------------------
    def subscribe(self, subscribeReq):
        """订阅行情，自动订阅全部行情，无需实现"""
        pass

    #----------------------------------------------------------------------
    def sendOrder(self, orderReq):
        """发单"""
        self.tradeApi.sendOrder(orderReq)

    #----------------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq):
        """撤单"""
        self.tradeApi.cancel(cancelOrderReq)

    #----------------------------------------------------------------------
    def qryAccount(self):
        """查询账户资金"""
        pass

    #----------------------------------------------------------------------
    def qryPosition(self):
        """查询持仓"""
        pass

    #----------------------------------------------------------------------
    def close(self):
        """关闭"""
        pass

    #----------------------------------------------------------------------
    def initQuery(self):
        """初始化连续查询"""
        pass

    #----------------------------------------------------------------------
    def query(self, event):
        """注册到事件处理引擎上的查询函数"""
        pass

    #----------------------------------------------------------------------
    def startQuery(self):
        """启动连续查询"""
        self.eventEngine.register(EVENT_TIMER, self.query)

    #----------------------------------------------------------------------
    def setQryEnabled(self, qryEnabled):
        """设置是否要启动循环查询"""
        self.qryEnabled = qryEnabled


########################################################################
'''
class StubTradeApi(vnstub.TradeApi):
    """交易接口"""

    #----------------------------------------------------------------------
    def __init__(self, gateway):
        """Constructor"""
        super(StubTradeApi, self).__init__()

        self.gateway = gateway
        self.gatewayName = gateway.gatewayName

        self.localID = 0            # 本地委托号
        self.localSystemDict = {}   # key:localID, value:systemID
        self.systemLocalDict = {}   # key:systemID, value:localID
        self.workingOrderDict = {}  # key:localID, value:order
        self.reqLocalDict = {}      # key:reqID, value:localID
        self.cancelDict = {}        # key:localID, value:cancelOrderReq

        self.tradeID = 0            # 本地成交号

    #----------------------------------------------------------------------
    def onError(self, error, req, reqID):
        """错误推送"""
        pass

    #----------------------------------------------------------------------
    def onGetAccountInfo(self, data, req, reqID):
        """查询账户回调"""
        # 推送账户数据
        pass
    #----------------------------------------------------------------------
    def onGetOrders(self, data, req, reqID):
        """查询委托回调"""
        pass

    #----------------------------------------------------------------------
    def onOrderInfo(self, data, req, reqID):
        """委托详情回调"""
        pass

    #----------------------------------------------------------------------
    def onBuy(self, data, req, reqID):
        """买入回调"""
        localID = self.reqLocalDict[reqID]
        systemID = data['id']
        self.localSystemDict[localID] = systemID
        self.systemLocalDict[systemID] = localID

        # 撤单
        if localID in self.cancelDict:
            req = self.cancelDict[localID]
            self.cancel(req)
            del self.cancelDict[localID]

        # 推送委托信息
        order = self.workingOrderDict[localID]
        if data['result'] == 'success':
            order.status = STATUS_NOTTRADED
        self.gateway.onOrder(order)

    #----------------------------------------------------------------------
    def onSell(self, data, req, reqID):
        pass

    #----------------------------------------------------------------------
    def onBuyMarket(self, data, req, reqID):
        """市价买入回调"""
        print(data)

    #----------------------------------------------------------------------
    def onSellMarket(self, data, req, reqID):
        """市价卖出回调"""
        print(data)

    #----------------------------------------------------------------------
    def onCancelOrder(self, data, req, reqID):
        """撤单回调"""
        pass

    #----------------------------------------------------------------------
    def onGetNewDealOrders(self, data, req, reqID):
        """查询最新成交回调"""
        print(data)

    #----------------------------------------------------------------------
    def onGetOrderIdByTradeId(self, data, req, reqID):
        """通过成交编号查询委托编号回调"""
        print(data)

    #----------------------------------------------------------------------
    def onWithdrawCoin(self, data, req, reqID):
        """提币回调"""
        print(data)

    #----------------------------------------------------------------------
    def onCancelWithdrawCoin(self, data, req, reqID):
        """取消提币回调"""
        print(data)

    #----------------------------------------------------------------------
    def onGetWithdrawCoinResult(self, data, req, reqID):
        """查询提币结果回调"""
        print(data)

    #----------------------------------------------------------------------
    def onTransfer(self, data, req, reqID):
        """转账回调"""
        print(data)

    #----------------------------------------------------------------------
    def onLoan(self, data, req, reqID):
        """申请杠杆回调"""
        print(data)

    #----------------------------------------------------------------------
    def onRepayment(self, data, req, reqID):
        """归还杠杆回调"""
        print(data)

    #----------------------------------------------------------------------
    def onLoanAvailable(self, data, req, reqID):
        """查询杠杆额度回调"""
        print(data)

    #----------------------------------------------------------------------
    def onGetLoans(self, data, req, reqID):
        """查询杠杆列表"""
        print(data)

    #----------------------------------------------------------------------
    def connect(self, accessKey, secretKey, market, debug=False):
        """连接服务器"""
        self.market = market
        self.DEBUG = debug

        self.init(accessKey, secretKey)

        # 查询未成交委托
        self.getOrders(vnstub.COINTYPE_BTC, self.market)

        if self.market == vnstub.MARKETTYPE_CNY:
            # 只有人民币市场才有莱特币
            self.getOrders(vnstub.COINTYPE_LTC, self.market)

    # ----------------------------------------------------------------------
    def queryWorkingOrders(self):
        """查询活动委托状态"""
        pass

    # ----------------------------------------------------------------------
    def queryAccount(self):
        """查询活动委托状态"""
        pass

    # ----------------------------------------------------------------------
    def sendOrder(self, req):
        """发送委托"""
        pass

    # ----------------------------------------------------------------------
    def cancel(self, req):
        """撤单"""
        pass


########################################################################
class StubDataApi(vnstub.DataApi):
    """行情接口"""

    #----------------------------------------------------------------------
    def __init__(self, gateway):
        """Constructor"""
        super(StubDataApi, self).__init__()

        self.market = 'cny'

        self.gateway = gateway
        self.gatewayName = gateway.gatewayName

        self.tickDict = {}      # key:symbol, value:tick


    #----------------------------------------------------------------------
    def onTick(self, data):
        """实时成交推送"""
        print(data)

    #----------------------------------------------------------------------
    def onQuote(self, data):
        pass

    #----------------------------------------------------------------------
    def onDepth(self, data):
        pass

    #----------------------------------------------------------------------
    def connect(self, interval, market, debug=False):
        """连接服务器"""
        pass
'''




