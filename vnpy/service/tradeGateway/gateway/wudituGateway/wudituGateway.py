# encoding: UTF-8

'''
vn.stub的gateway接入
'''



from vnpy.service.vtGateway import VtGateway
from vnpy.service.main.vtObject import VtLogData, VtTickData
from vnpy.service.vtGateway import *
from vnpy.service.language.vtConstant import *
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import threading
import tushare as ts
#import pymongo
import json
import datetime #导入日期时间模块
import pymongo
#import errors
#import numpy as np
import pandas as pd
from pymongo import MongoClient
from vnpy.service.event import EventEngine

########################################################################
class WudituGateway(VtGateway):
    """wuditu的接口,包括交易接口（东财），实时数据接口（tushare）"""

    #----------------------------------------------------------------------
    def __init__(self, eventEngine, gatewayName='wuditu'):
        """Constructor"""

        super(WudituGateway, self).__init__(eventEngine, gatewayName)

        self.market = 'gupiao'

        # 交易api，提供交易接口
        self.tradeApi = WudituTradeApi(self)
        # self.tradeApi.webInit()

        # 行情api，采用定时器获取实时行情数据
        self.dataApi = WudituDataApi(self)
        
        # 股票标的字典
        self.dataApi.onBaseStockDict()


    #----------------------------------------------------------------------
    def onStart(self):
        """启动数据接口"""
        self.dataApi.onStart()



    def onUpdateTask(self, task):
        """更新任务"""
        self.dataApi.onUpdateTask(task)


    #----------------------------------------------------------------------
    def writeLog(self, content):
        """发出日志"""
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = content
        self.onLog(log)

    #----------------------------------------------------------------------
    def sendOrder(self, orderReq):
        """发单"""
        print('fadan', orderReq)

        #单子方向, 买  卖
        #vtObject.VtOrderData
        #self.symbol = EMPTY_STRING              # 合约代码
        #self.exchange = EMPTY_STRING            # 交易所代码, 使用该代码代表股票代码

        '''
        if orderReq.direction == DIRECTION_LONG:
            self.tradeApi.onBuy(orderReq.exchange, orderReq.price, orderReq.volume)
        else:
            self.tradeApi.onSell(orderReq.exchange, orderReq.price, orderReq.volume)
        '''
        #self.tradeApi.onBuy(orderReq.price, orderReq.price, orderReq.price, orderReq.price)


    #----------------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq):
        """撤单"""
        print(cancelOrderReq)
        #self.tradeApi.cancel(cancelOrderReq)

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
        self.tradeApi.exit()
        self.dataApi.exit()

    #----------------------------------------------------------------------
    def initQuery(self):
        """初始化连续查询"""
        if self.qryEnabled:
            self.qryFunctionList = [self.tradeApi.queryWorkingOrders, self.tradeApi.queryAccount]
            self.startQuery()

    #----------------------------------------------------------------------
    def query(self, event):
        """注册到事件处理引擎上的查询函数"""
        print('timer test')
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
class WudituTradeApi(object):
    """交易接口，东方财富"""

    #----------------------------------------------------------------------
    def __init__(self, gateway=''):
        """Constructor"""
        #super(MyTradeApi, self).__init__()
        if gateway != '':
            self.gateway = gateway
            self.gatewayName = gateway.gatewayName

        self.localID = 0            # 本地委托号
        self.localSystemDict = {}   # key:localID, value:systemID
        self.systemLocalDict = {}   # key:systemID, value:localID
        self.workingOrderDict = {}  # key:localID, value:order
        self.reqLocalDict = {}      # key:reqID, value:localID
        self.cancelDict = {}        # key:localID, value:cancelOrderReq

        self.tradeID = 0            # 本地成交号

        self.filename = 'cookie.txt'
        self.browser = ''
        self.firefoxProfile = ''
        self.url = 'https://jy.xzsec.com/'
        #self.url = 'https://www.baidu.com/'
        #self.url = 'file:///E:/1.3%20python%20%E6%8A%80%E6%9C%AF%E6%80%BB%E7%BB%93%E5%8F%82%E8%80%83/11.0%20dongcai%E4%BA%A4%E6%98%93%E8%BD%AF%E4%BB%B6/test.htm'



        #self.appHandle = self.getWindowsHandle(self.processName)
        self.timestamp =str(int(time.time()*1000))


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

    #get 买入页面
    #'tradeType': 'B'  现价买入
    #'tradeType': '0a'  对手方最优价格申报
    #'tradeType': '0b'  本方最优价格申报
    #'tradeType': '0c'  即使申报剩余撤销申报
    #'tradeType': '0d'  最优五档即使申报剩余撤销申报
    #'tradeType': '0e'  全额成交或撤销申报
    #----------------------------------------------------------------------
    def onBuy(self, stockCode, price, amount):
        """买入回调"""



        #ready for buy
        time.sleep(0.5)
        self.browser.find_elements_by_link_text("普通")[0].click()
        self.browser.find_elements_by_link_text("买入")[0].click()

        #stock
        time.sleep(0.5)
        self.browser.find_element_by_id("stockCode").clear()
        self.browser.find_element_by_id("stockCode").send_keys(stockCode)


        #模拟点击 tb list的第一个元素， 证券代码的一个显示
        time.sleep(0.5)
        td = self.browser.find_elements_by_css_selector("td > span")
        print('td,span', td, type(td))
        td[0].click()




        #委托方式
        time.sleep(0.5)
        #tradeType = 'B' #如需修改成其他方式，参考下面

        #定位到要点击的元素
        #完整的xpath，//div[@id='main']/div/div[2]/div[2]/div[2]/div[3]/div/div/ul/li[4]
        #最后li列表的下表是选择项，通过selenium ide 抓取定位方式
        # 现价买入 --- //div[3]/div/div/ul/li
        # 对手方最优价格申报 --- //div[3]/div/div/ul/li[2]
        # ....
        # 全额成交或撤销申报 --- //div[3]/div/div/ul/li[6]
        tradeType = 'B'
        #sel = self.browser.find_elements_by_css_selector("div.select_showbox")
        #print('sel', sel, type(sel))
        sel = self.browser.find_element_by_xpath("//div[3]/div/div/ul/li")
        print('sel', sel, type(sel))

        #输入价格
        time.sleep(0.5)
        if tradeType == 'B':
            self.browser.find_element_by_id("iptPrice").clear()
            self.browser.find_element_by_id("iptPrice").send_keys(price)
            print(tradeType)

        #买入数量
        time.sleep(0.5)
        self.browser.find_element_by_id("iptCount").clear()
        self.browser.find_element_by_id("iptCount").send_keys(amount)


        #点击买入按钮
        time.sleep(0.5)
        btnConfirm = self.browser.find_element_by_id("btnConfirm")
        if btnConfirm.get_attribute('disabled') == 'true':
            print('买入按钮',"btnConfirm disabled")
            return
        else:
            print('买入按钮', btnConfirm.get_attribute('disabled'))
            btnConfirm.click()


    #get 卖出页面
    #'tradeType': 'S'  现价卖出
    #'tradeType': '0f'  对手方最优价格申报
    #'tradeType': '0g'  本方最优价格申报
    #'tradeType': '0h'  即使申报剩余撤销申报
    #'tradeType': '0i'  最优五档即使申报剩余撤销申报
    #'tradeType': '0j'  全额成交或撤销申报
    #----------------------------------------------------------------------
    def onSell(self, stockCode, price, amount):
        """卖出回调"""

        #ready for buy
        time.sleep(0.5)
        if self.webCheckLogin() == False:
            return

        if self.browser.current_url != 'https://jy.xzsec.com/Trade/Sale':
            self.browser.find_elements_by_link_text("普通")[0].click()
            self.browser.find_elements_by_link_text("卖出")[0].click()

        #stock
        time.sleep(0.5)
        self.browser.find_element_by_id("stockCode").clear()
        self.browser.find_element_by_id("stockCode").send_keys(stockCode)
        #self.browser.find_element_by_id("stockCode").send_keys(Keys.ENTER)


        #模拟点击 tb list的第一个元素
        time.sleep(0.5)
        td = self.browser.find_elements_by_css_selector("td > span")
        print('td,span', td, type(td))
        td[0].click()



        #委托方式
        time.sleep(0.5)
        #tradeType = 'S' #如需修改成其他方式，参考下面

        #定位到要点击的元素
        #完整的xpath，//div[@id='main']/div/div[2]/div[2]/div[2]/div[3]/div/div/ul/li[4]
        #最后li列表的下表是选择项，通过selenium ide 抓取定位方式
        # 现价买入 --- //div[3]/div/div/ul/li
        # 对手方最优价格申报 --- //div[3]/div/div/ul/li[2]
        # ....
        # 全额成交或撤销申报 --- //div[3]/div/div/ul/li[6]
        tradeType = 'S'
        #sel = self.browser.find_elements_by_css_selector("div.select_showbox")
        #print('sel', sel, type(sel))
        sel = self.browser.find_element_by_xpath("//div[3]/div/div/ul/li")
        print('sel', sel, type(sel))



        #输入价格
        time.sleep(0.5)
        if tradeType == 'S':
            self.browser.find_element_by_id("iptPrice").clear()
            self.browser.find_element_by_id("iptPrice").send_keys(price)
            print(tradeType)


        #输入买入数量
        time.sleep(0.5)
        self.browser.find_element_by_id("iptCount").clear()
        self.browser.find_element_by_id("iptCount").send_keys(amount)


        #点击卖出按钮
        time.sleep(0.5)
        btnConfirm = self.browser.find_element_by_id("btnConfirm")
        if btnConfirm.get_attribute('disabled') == 'true':
            print('卖出按钮:',"btnConfirm disabled")
            return
        else:
            print('卖出按钮:', btnConfirm.get_attribute('disabled'))
            btnConfirm.click()


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
    def onTransfer(self, data, req, reqID):
        """转账回调"""
        print(data)


    #----------------------------------------------------------------------
    def connect(self, accessKey, secretKey, market, debug=False):
        """连接服务器"""

        self.webInit()
        #self.webInitLoaclPage()


        print('请登陆')

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


    #----------------------------------------------------------------------
    def webInit(self):
        '''初始化浏览器'''

        print('webInit')

        #通过在开始菜单中的“搜索程序和文件”中输入%APPDATA%\Mozilla\Firefox\Profiles\ 来获取路径
        self.firefoxProfile = webdriver.FirefoxProfile(r'C:\Users\chen\AppData\Roaming\Mozilla\Firefox\Profiles\9fvo25z9.default')
        self.browser = webdriver.Firefox(self.firefoxProfile)

        #方式2 打开的Firefox浏览器将是不带任何插件的浏览器，和初始安装一样的状态。
        #这个使用本地页面时会死循环
        #self.browser = webdriver.Firefox()

        #3.
        #self.browser.maximize_window() #将浏览器最大化显示

        # 隐性等待，最长等30秒
        self.browser.implicitly_wait(20)  # seconds
        self.browser.set_page_load_timeout(10)
        try:
            self.browser.get(self.url)
        except TimeoutException:
            print ('time out after 30 seconds when loading page')

            #当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            #self.browser.execute_script('window.stop()')

        #self.browser.get(self.url)
        #locator = EC.title_contains(u"新标签页")
        print('open URL success')
        try:
            self.browser.get(self.url)
            WebDriverWait(self.browser, 10, 1).until(EC.title_contains(u"百度一下"))
            print('wait for url')
        except TimeoutException:
            print ('time out after 30 seconds when loading page')
        #time.sleep(2)

        self.appHandle=self.browser.current_window_handle
        print('now handle', self.appHandle)

        #print('command_executor', dir(self.browser.command_executor))
        print('_url', self.browser.command_executor._url)

        #print('desired_capabilities', self.browser.desired_capabilities)

    #----------------------------------------------------------------------
    def exit(self):
        '''退出浏览器'''

        #self.browser.close()
        time.sleep(1)
        if self.browser != '':
            self.browser.quit()
        #print(self.browser.toString)


    #----------------------------------------------------------------------
    def webCheckLogin(self):
        '''检查是否已经登录'''

        if self.browser == '':
            return False

        #设置成买入页面, 如果能够设置成功，说明登陆时ok的
        self.browser.get("https://jy.xzsec.com/Trade/Buy")
        time.sleep(1)
        if self.browser.current_url == 'https://jy.xzsec.com/Trade/Buy':
            return True
        else:
            return False

    def setNormalBuyPage(self):
        '''跳转普通账户，买入页面'''
        self.browser.get("https://jy.xzsec.com/Trade/Buy")


    def setNormalSellPage(self):
        '''跳转普通账户，卖出页面'''
        self.browser.get("https://jy.xzsec.com/Trade/Sale")

    def setCreditBuyPage(self):
        '''跳转信用账户'''
        self.browser.get("https://jy.xzsec.com/MarginTrade/Buy")


########################################################################
class WudituDataApi(object):
    """数据接口接口，使用tushare实时数据接口"""

    #----------------------------------------------------------------------
    def __init__(self, gateway = ''):
        """Constructor"""
        #super(WudituDataApi, self).__init__()

        self.market = 'tushare'
        print('gateway:', gateway)

        if gateway != '':
            self.gateway = gateway
            self.gatewayName = gateway.gatewayName
        else:
            self.gateway = ''
            self.gatewayName = ''


        # tick数据字典， key：code v: tickdata
        self.tickDict = {}     # 股票代码列表
        self.tickCodeList = []     # 股票代码列表
        
        
        
        self.stockDict = {}     # 股票代码列表
        
        
        self.timerRun = False


        # timer处理线程
        '''
        self.__tickTimerPeriod = 5   # 5 second
        self.__tickTimer = threading.Timer(self.__tickTimerPeriod, self.__onTimer)
        self.__tickTimer.setDaemon(True)
        #self.__tickTimer.join()
        self.__tickTimer.start()
        print('tickTimer start!, isDaemon:', self.__tickTimer.isDaemon())
        '''


    #----------------------------------------------------------------------
    def __del__(self):
        self.onStop()


    #----------------------------------------------------------------------
    def __onTimer(self):

        """引擎运行"""
        #print('Hello Timer!', self.__tickTimer.isDaemon())
        self.onTick()

        if len(self.tickCodeList) == 0:
            self.onStop()
            return

        # start timer
        self.__tickTimer = threading.Timer(self.__tickTimerPeriod, self.__onTimer)
        self.__tickTimer.setDaemon(True)
        self.__tickTimer.start()

    #----------------------------------------------------------------------
    def onStart(self):
        # timer处理线程
        self.__tickTimerPeriod = 5   # 5 second
        self.__tickTimer = threading.Timer(self.__tickTimerPeriod, self.__onTimer)
        self.__tickTimer.setDaemon(True)
        #self.__tickTimer.join()
        self.__tickTimer.start()

        self.timerRun = True
        print('tickTimer start!, isDaemon:', self.__tickTimer.isDaemon())

    #----------------------------------------------------------------------
    def onStop(self):
        if self.timerRun == True:
            self.__tickTimer.cancel()
        self.timerRun = False
        print('tickTimer cancel!')

    #----------------------------------------------------------------------
    def onUpdateTask(self, task):
        """更新任务"""

        code = task.code
        self.tickCodeList.append(code)

        # list去重
        self.tickCodeList = list(set(self.tickCodeList))
        print('tickCodeList:', self.tickCodeList)


    #----------------------------------------------------------------------
    def onTick(self):
        """实时深度推送"""
        print('Hello Timer!', self.tickCodeList)

        ## get_realtime_quotes
        try:
            df = ts.get_realtime_quotes(self.tickCodeList)
            #print(df)
            if df.empty:
                print("data is null")
            else:
            #DataForm格式数据, 数据格式转换为vnpy

                for rowIndex, item in enumerate(df.index):
                    code = df.iloc[rowIndex]['code']
                    #print(code)

                    if code not in self.tickDict:
                        tick = VtTickData()
                        tick.gatewayName = self.gatewayName
                         
                        # 添加到字典中
                        self.tickDict[code] = tick
                    else:
                        tick = self.tickDict[code]

                    # tick数据，格式封装成vnpy格式
                    tick.code = code
                    tick.vtSymbol = code
                    tick.lastPrice = df.iloc[rowIndex]['bid']            # 最新成交价
                    tick.lastVolume = df.iloc[rowIndex]['b1_v']             # 最新成交量
                    tick.volume = df.iloc[rowIndex]['volume']                 # 今天总成交量
                    tick.name = df.iloc[rowIndex]['name']                 # 代码名称
                    #tick.openInterest = EMPTY_INT           # 持仓量
                    tick.time = df.iloc[rowIndex]['time']
                    tick.date = df.iloc[rowIndex]['date']
                    #tick.datetime = None                    # python的datetime时间对象

                    # 常规行情
                    tick.openPrice = df.iloc[rowIndex]['open']            # 今日开盘价
                    tick.highPrice = df.iloc[rowIndex]['high']            # 今日最高价
                    tick.lowPrice = df.iloc[rowIndex]['low']             # 今日最低价
                    tick.preClosePrice = df.iloc[rowIndex]['pre_close']

                    #tick.upperLimit = EMPTY_FLOAT           # 涨停价
                    #tick.lowerLimit = EMPTY_FLOAT           # 跌停价


                    # 五档行情
                    tick.bidPrice1 = df.iloc[rowIndex]['b1_p']
                    tick.bidPrice2 = df.iloc[rowIndex]['b2_p']
                    tick.bidPrice3 = df.iloc[rowIndex]['b3_p']
                    tick.bidPrice4 = df.iloc[rowIndex]['b4_p']
                    tick.bidPrice5 = df.iloc[rowIndex]['b5_p']

                    tick.askPrice1 = df.iloc[rowIndex]['a1_p']
                    tick.askPrice2 = df.iloc[rowIndex]['a2_p']
                    tick.askPrice3 = df.iloc[rowIndex]['a3_p']
                    tick.askPrice4 = df.iloc[rowIndex]['a4_p']
                    tick.askPrice5 = df.iloc[rowIndex]['a5_p']


                    tick.bidVolume1 = df.iloc[rowIndex]['b1_v']
                    tick.bidVolume2 = df.iloc[rowIndex]['b2_v']
                    tick.bidVolume3 = df.iloc[rowIndex]['b3_v']
                    tick.bidVolume4 = df.iloc[rowIndex]['b4_v']
                    tick.bidVolume5 = df.iloc[rowIndex]['b5_v']

                    tick.askVolume1 = df.iloc[rowIndex]['a1_v']
                    tick.askVolume2 = df.iloc[rowIndex]['a2_v']
                    tick.askVolume3 = df.iloc[rowIndex]['a3_v']
                    tick.askVolume4 = df.iloc[rowIndex]['a4_v']
                    tick.askVolume5 = df.iloc[rowIndex]['a5_v']


        except pymongo.errors.DuplicateKeyError:
            print("DuplicateKey")

        self.gateway.onTick(tick)

   #----------------------------------------------------------------------
    def onBaseStockDict(self):
        """获取有效的股票字典"""
        print('onBaseStockList!', self.stockDict)

        ## get_realtime_quotes
        try:
            df = ts.get_stock_basics()
            #print(df)
            if df.empty:
                print("data is null")
            else:
                #DataForm格式数据, 数据格式转换为vnpy
                for index, item in enumerate(df.index):
                    code = item
                    name = df.iloc[index]['name']
                    self.stockDict[code] = name
                    #print('stockDict:', code, name)


        except pymongo.errors.DuplicateKeyError:
            print("DuplicateKey")


        self.gateway.onObjDict(self.stockDict)


    def exit(self):
        """exit"""
        self.onStop()


#----------------------------------------------------------------------
def test():

    #trade api
    wudituTrade = WudituTradeApi()
    #wudituTrade.webInit()
    #web.webInitLoaclPage()

    #data api
    wudituData = WudituDataApi()
    print('请登陆')
    try:
        while 1:

            num = input('输入测试流程： ')
            if num == '9':
                wudituTrade.exit()
                break

            # 检查是否处于登陆状态，如果没有登陆，需要重新登陆
            flag = wudituTrade.webCheckLogin()
            #print('webCheckLogin', flag)
            if flag == False:
                print('登陆失败，请重新登陆')
                continue

            # 测试流程
            if num == '1':
                #用户手工登陆，验证码无法自动识别
                #web.webLogin()
                pass
            elif num == '2':
                wudituTrade.setNormalBuyPage()
            elif num == '3':
                wudituTrade.setCreditBuyPage()
            elif num == '4':
                wudituTrade.setNormalSellPage()
            elif num == '5':
                wudituTrade.onBuy('002500', '11.00', '100')
            elif num == '6':
                wudituTrade.onSell('002500', '12.01', '100')

    except:
        print('except')
    finally:
        print('EXIT')
        wudituData.__del__()

if __name__ == '__main__':

    #test2()
    test()

    #web = WebManager()
    #web.webInit()



