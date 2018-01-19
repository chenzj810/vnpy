# encoding: UTF-8

'''
vn.stub的gateway接入
'''



from vnpy.trader.gatewayTrade.vtGateway import VtGateway
from vnpy.trader.main.vtObject import VtLogData, VtTickData
from vnpy.trader.gatewayTrade.vtGateway import *
from vnpy.trader.language.vtConstant import *
from vnpy.trader.event.eventEngine import EventEngine
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

#

########################################################################
class EastMoneyTradeApi(VtGateway):
    """交易接口，东方财富"""

    #----------------------------------------------------------------------
    def __init__(self, eventEngine, dbClient=None):
        """Constructor"""

        super(EastMoneyTradeApi, self).__init__(eventEngine, dbClient)
        if dbClient != None:
            #self.gateway = gatewayName
            self.dbClient = dbClient


        print('EastMoneyTradeApi:', dbClient)

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



