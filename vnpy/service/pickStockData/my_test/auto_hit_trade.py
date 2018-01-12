# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 10:25:30 2017

@author: chen
"""

import pyautogui
import time
import os
from run_trade_app import AppRunManager

########################################################################
class TradeManager(object):
    """交易管理"""
    className = 'app 应用程序'
    author = u'chenzejun'

    processPwd='810523'

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.screenWidth, self.screenHeight = pyautogui.size()
        self.currentMouseX, self.currentMouseY = pyautogui.position()
        print(self.screenWidth, self.screenHeight)
        print(self.currentMouseX, self.currentMouseY)


        self.appPath='C:\eastmoney\swc8\EmTrade\EmTrade.exe PC_Free'
        self.appManager = AppRunManager(self.appPath)


    #----------------------------------------------------------------------
    def run(self):
        """run"""
        os.system(self.appPath)


    #----------------------------------------------------------------------
    def getLoginPosition(self):
        """获取登陆位置"""

        loginLocation = pyautogui.locateOnScreen('denglu.png')
        print(loginLocation)

    #----------------------------------------------------------------------
    def isLogin(self):
        """判断是否登陆"""
        loginLocation = pyautogui.locateOnScreen('lockpage.png')
        if loginLocation is None:
            print('窗口已登陆')
            return 1
        else:
            print('窗口没有登陆')
            return 0

    #----------------------------------------------------------------------
    def tryLogin(self):
        """尽力登陆"""

        print('准备login')
        if self.isLogin():
            return

        """窗口最大化后，模拟点击空白区域，使光标定位到密码输入框"""
        pyautogui.moveTo(316, 37)#模拟点击空白区域
        pyautogui.click()

        #m没有登陆的情况下，输入密码
        pyautogui.typewrite(self.processPwd, interval=0.25)
        time.sleep (1.0)
        pyautogui.press('enter')



    #----------------------------------------------------------------------
    def clickStockMode(self):
        """点击股票标签"""
        pyautogui.moveTo(20, 68)#点击股票标签
        pyautogui.click()
        time.sleep(0.5)

    #----------------------------------------------------------------------
    def clickBuyButton(self):
        """点击买入按钮"""
        pyautogui.moveTo(34, 132)#点击买入按钮
        pyautogui.click()
        time.sleep(0.5)

    #----------------------------------------------------------------------
    def inputBuyOrder(self, symbol, price, volume):
        """输入股票买单"""

        ####1.点击证券代码框
        pyautogui.moveTo(300, 73)
        pyautogui.doubleClick()
        time.sleep(0.5)

        #输入股票代码
        pyautogui.typewrite(symbol, interval=0.25)
        time.sleep(0.5)



        ####2.点击买入代码框
        pyautogui.moveTo(300, 158)
        pyautogui.doubleClick()
        time.sleep(0.5)

        #输入股票代码
        pyautogui.typewrite(price, interval=0.25)
        time.sleep(0.5)




        ####3.点击买入数量框
        pyautogui.moveTo(300, 212)
        pyautogui.doubleClick()
        time.sleep(0.5)

        #输入股票代码
        pyautogui.typewrite(volume, interval=0.25)
        time.sleep(0.5)


        ####4.点击买入按钮，下单
        pyautogui.moveTo(349, 275)
        #pyautogui.click()
        time.sleep(0.5)
        pyautogui.press('enter')

        time.sleep(1)



    #----------------------------------------------------------------------
    def sendBuyOrder(self, symbol, price, volume):
        result = self.appManager.setForegroundWindow()
        if result==1:
            #time.sleep (3.0)

            #准备并输入密码
            self.tryLogin()
            self.clickStockMode()
            self.clickBuyButton()

            ##如果有告警窗口，点击关闭
            if self.appManager.getAlarmWindowsHandle():
                pyautogui.press('enter')
                time.sleep(0.5)

            ##下买单
            self.inputBuyOrder(symbol, price, volume)

            if self.appManager.getOrderWindowsHandle():
                pyautogui.press('enter')
                time.sleep(0.5)
                print('下单成功, 股票：', symbol, '价格：', price, '数量：', volume)

        else:
            print('窗口获取焦点失败，应用程序未启动')


########################################################################
#----------------------------------------------------------------------
def positionRecord():
    """光标记录"""
    print('Press Ctrl-C to quit')
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: {} Y: {}'.format(*[str(x).rjust(4) for x in [x, y]])
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')

#----------------------------------------------------------------------
def test():
    """测试函数"""
    tradeManager = TradeManager()
    tradeManager.sendBuyOrder('002500', '10.63', '100')




"""""entry"""""
if __name__ == '__main__':
    positionRecord()
    #test()

'''
screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()
time.sleep(30)
pyautogui.moveTo(279, 364)#打开品种
pyautogui.click()
time.sleep(0.5)
pyautogui.moveTo(231, 429)#选品种枸杞
pyautogui.click()
time.sleep(0.5)
pyautogui.moveTo(381, 368)#选择买卖方向
pyautogui.click()
time.sleep(0.5)
pyautogui.moveTo(342, 405)#选择卖出
pyautogui.click()
time.sleep(0.5)
pyautogui.moveTo(342, 405)#选择卖出
pyautogui.click()
time.sleep(0.5)
pyautogui.moveTo(513, 368)#选择开平仓
pyautogui.click()
time.sleep(0.5)
pyautogui.moveTo(461,405)#选择平仓
pyautogui.click()
time.sleep(0.5)
pyautogui.moveTo(614,367)#选择价格
pyautogui.doubleClick()
time.sleep(0.1)
pyautogui.press('delete')
time.sleep(0.1)
pyautogui.typewrite('180')
time.sleep(0.5)
pyautogui.moveTo(735,369)#选择价格
pyautogui.click()
time.sleep(0.1)
pyautogui.click()
time.sleep(0.1)
pyautogui.doubleClick()
pyautogui.press('delete')
time.sleep(0.1)
pyautogui.typewrite('1')
time.sleep(0.5)
pyautogui.moveTo(905,365)
pyautogui.click()
'''