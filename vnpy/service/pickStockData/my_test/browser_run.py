# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 09:49:00 2017

@author: chen
"""

#import  selenium
import pyautogui
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import win32api
import win32com.client
import win32con
import win32gui
import win32process
import subprocess
import pickle
from ctypes import *

## 这段代码是用于解决中文报错的问题
#reload(sys)
#sys.setdefaultencoding("utf8")
#####################################################
#


class WebManager(object):


    className = 'app 应用程序'
    author = u'chenzejun'

    appPath='C:\Program Files (x86)\Mozilla Firefox'
    processName='Firefox'

    #----------------------------------------------------------------------
    def __init__(self):
        self.name = '540800288762'
        self.passwprd = '810523'
        self.captcha = ''
        self.validatekey = '94783938-d9c3-4219-a013-5d828e469353'
        self.filename = 'cookie.txt'
        self.browser = ''
        self.desired_capabilities = ''

        self.url = 'https://jy.xzsec.com/'
        #self.url = 'https://www.baidu.com/'
        #self.url = 'file:///E:/1.3%20python%20%E6%8A%80%E6%9C%AF%E6%80%BB%E7%BB%93%E5%8F%82%E8%80%83/11.0%20dongcai%E4%BA%A4%E6%98%93%E8%BD%AF%E4%BB%B6/test.htm'



        #self.appHandle = self.getWindowsHandle(self.processName)
        self.timestamp =str(int(time.time()*1000))



    #----------------------------------------------------------------------
    def webDriverSave(self):
        '''保存diriver'''

        # 保存验证码到本地
        #cfgfile = open('e:/handle.pkl', 'wb')
        with open('e:/handle.pkl', 'wb') as cfgfile:
            pickle.dump(self.browser.desired_capabilities, cfgfile)
        #cfgfile.close()
        #print (self.browser.desired_capabilities)



    #----------------------------------------------------------------------
    def webDriverRead(self):
        '''读取driver内容'''

        # 保存验证码到本地
        #try:
        #    cfgfile = open('e:/handle.pkl', 'rb')
        #    self.browser = pickle.load(cfgfile)
        #    cfgfile.close()
        #    print(self.browser)
        #except (FileNotFoundError,EOFError):
        #    print('not found file, e:/handle.pkl')
        with open('e:/handle.pkl', 'rb') as cfgfile:
            self.desired_capabilities = pickle.load(cfgfile)

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
    def webSave(self):
        '''初始化浏览器'''

        #self.webDriverRead()
        print('webinit')
        if self.desired_capabilities != '':
            print('already has browser', self.desired_capabilities)

        else:
            self.webInitNewBrowser()
            print('new init browser', self.browser)
            self.webDriverSave()

 #----------------------------------------------------------------------
    def webInitLoaclPage(self):
        '''初始化浏览器'''

        self.browser = webdriver.Firefox()
        print('webInitLoaclPage:', self.browser)
        #self.browser.maximize_window() #将浏览器最大化显示

        self.url = 'file:///E:/1.3%20python%20%E6%8A%80%E6%9C%AF%E6%80%BB%E7%BB%93%E5%8F%82%E8%80%83/11.0%20dongcai%E4%BA%A4%E6%98%93%E8%BD%AF%E4%BB%B6/test.htm'
        self.browser.get(self.url)
        time.sleep(2)



    #----------------------------------------------------------------------
    def webExit(self):
        '''退出浏览器'''

        #self.browser.close()
        time.sleep(3)
        self.browser.quit()
        #print(self.browser.toString)



    #----------------------------------------------------------------------
    def webPrintAttibutes(self):
        '''打印驱动属性列表'''

        title = self.browser.title
        print ('title', title)

        now_url = self.browser.current_url
        print ('now_url', now_url)

        print ('session_id', self.browser.session_id)
        print ('window_handles', self.browser.window_handles)


        print ('driver attributes:')
        print (dir(self.browser))

    #----------------------------------------------------------------------
    def webLogin(self):
        '''登录网站'''

        #loop login, 循环登陆 ， 5次
        for i in range(5):
            #用户名
            self.browser.find_element_by_id("txtZjzh").clear()
            self.browser.find_element_by_id("txtZjzh").send_keys(self.name)

            time.sleep(0.5)

            #passwd
            self.browser.find_element_by_id("txtPwd").clear()
            self.browser.find_element_by_id("txtPwd").send_keys(self.passwprd)

            #单选框，3小时
            #self.browser.find_element_by_id("rdsc45").clear()
            self.browser.find_element_by_id("rdsc45").click()


            # 保存验证码到本地, 手动输入
            result = self.browser.find_element_by_id("imgValidCode")
            print('imgValidCode', result)
            #result.show()

            self.captcha = input('输入验证码： ')
            print(self.captcha)


            #验证码
            self.browser.find_element_by_id("txtValidCode").clear()
            self.browser.find_element_by_id("txtValidCode").send_keys(self.captcha)


            #点击登录按钮
            self.browser.find_element_by_id("btnConfirm").click()


            if self.webCheckLogin() == True:
                break



    #get 买入页面
    #'tradeType': 'B'  现价买入
    #'tradeType': '0a'  对手方最优价格申报
    #'tradeType': '0b'  本方最优价格申报
    #'tradeType': '0c'  即使申报剩余撤销申报
    #'tradeType': '0d'  最优五档即使申报剩余撤销申报
    #'tradeType': '0e'  全额成交或撤销申报
    #----------------------------------------------------------------------
    def sendBuyOrder(self, stockCode, price, amount, name):
        '''发送买单'''
        #self.setNormalBuyPage()

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

        '''
        #模拟点击 委托方式 标签
        time.sleep(0.5)
        label_list = self.browser.find_elements_by_tag_name("label")
        for opt in label_list:
            #print('label', opt,  opt.text)

            #定位到要点击的元素 委托方式"
            #模拟双击一下，自动填充证券名称等信息
            if opt.text == '委托方式:':
                print('点击', opt.text)
                #opt.click()
                #对定位到的元素执行鼠标右键操作
                ActionChains(self.browser).double_click(opt).perform()
                break
        '''

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

        #价格
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
    def sendSellOrder(self, stockCode, price, amount, name):
        '''发送卖单'''
        #self.setNormalSellPage()

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


        '''
        #模拟点击 委托方式 标签
        time.sleep(0.5)
        label_list = self.browser.find_elements_by_tag_name("label")
        for opt in label_list:
            #print('label', opt,  opt.text)

            #定位到要点击的元素 委托方式"
            #模拟双击一下，自动填充证券名称等信息
            if opt.text == '委托方式:':
                print('点击', opt.text)
                #opt.click()
                #对定位到的元素执行鼠标右键操作
                ActionChains(self.browser).double_click(opt).perform()
                break
        '''

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
    def webCheckLogin(self):
        '''检查是否已经登录'''

        #设置成买入页面, 如果能够设置成功，说明登陆时ok的
        self.browser.get("https://jy.xzsec.com/Trade/Buy")
        time.sleep(1)
        if self.browser.current_url == 'https://jy.xzsec.com/Trade/Buy':
            return True
        else:
            return False


#----------------------------------------------------------------------
def test():

    web = WebManager()
    web.webInit()
    #web.webInitLoaclPage()


    print('请登陆')
    while 1:

        num = input('输入测试流程： ')

        # 检查是否处于登陆状态，如果没有登陆，需要重新登陆
        flag = web.webCheckLogin()
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
            web.setNormalBuyPage()
        elif num == '3':
            web.setCreditBuyPage()
        elif num == '4':
            web.setNormalSellPage()
        elif num == '5':
            web.sendBuyOrder('002500', '11.00', '100', '山西证券')
        elif num == '6':
            web.sendSellOrder('002500', '12.01', '100', '山西证券')
        elif num == '8':
            web.webPrintTitle()
        elif num == '9':
            web.webExit()
            break




if __name__ == '__main__':

    #test2()
    test()
    #web = WebManager()
    #web.webInit()


