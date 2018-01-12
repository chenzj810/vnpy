# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 10:52:47 2017

@author: chen
"""

import os
import win32api
import win32com.client
import win32con
import win32gui
import win32process
import subprocess
import time

class AppRunManager(object):
    """app运行函数"""
    className = 'app 应用程序'
    author = u'chenzejun'

    appPath='C:\eastmoney\swc8\EmTrade\EmTrade.exe PC_Free'
    processName='东方财富证券'

    #----------------------------------------------------------------------
    def __init__(self, appPath):
        """Constructor"""
        if appPath !='':
            self.appPath = appPath
        print(self.appPath)
        self.appHandle = self.getWindowsHandle()


    #----------------------------------------------------------------------
    def run(self):
        """run"""
        os.system(self.appPath)


    #----------------------------------------------------------------------
    def run32(self):
        """run32"""
        # 打开本程序，在后台运行，即显示本程序的窗口
        #win32api.ShellExecute(0, 'open', self.appPath, '','',0)

        # 打开本程序，在前台运行
        win32api.ShellExecute(0, 'open', self.appPath, '','',1)

    #----------------------------------------------------------------------
    def runPopen(self):
        """run by popen"""
        self.appHandle = subprocess.Popen(self.appPath)
        return self.appHandle

    #----------------------------------------------------------------------
    def getWindowsHandle(self):
        """运行程序，如果程序存在，设置程序获得焦点"""
        hwnd=win32gui.FindWindow(None, self.processName)
        print(self.processName, hwnd)
        return hwnd


    #----------------------------------------------------------------------
    def getAlarmWindowsHandle(self):
        """运行程序，如果程序存在，设置程序获得焦点"""
        hwnd=win32gui.FindWindow(None, '警告')
        if hwnd > 0:
            print('有警告窗口', hwnd)
        return hwnd

    #----------------------------------------------------------------------
    def getOrderWindowsHandle(self):
        """运行程序，如果程序存在，设置程序获得焦点"""
        hwnd=win32gui.FindWindow(None, '提示信息')
        if hwnd > 0:
            print('有提示信息窗口，委托成功', hwnd)
        return hwnd

    def setMaximizeWindow(self):
        """设置窗口最大化"""
        win32gui.ShowWindow(self.appHandle, win32con.SW_MAXIMIZE)

    #----------------------------------------------------------------------
    def setForegroundWindow(self):
        """运行程序，如果程序存在，设置程序获得焦点"""

        if self.appHandle == 0:
            print('没有这个程序')
            return 0

        #
        # sleep to give the window time to appear
        #
        time.sleep (0.5)
        self.setMaximizeWindow()
        win32gui.SetForegroundWindow(self.appHandle)
        print('设置窗口到前台')
        return 1



    def CheckProcExistByPN(self, process_name):
        """运行程序，如果程序存在，设置程序获得焦点"""
        WMI = win32com.client.GetObject('winmgmts:')
        processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
        if len(processCodeCov) > 0:
            print (process_name + " exist")
            return 1
        else:
            print (process_name + " is not exist")
        return 0

    #----------------------------------------------------------------------
    def inputPassword(self):
        """输入密码"""
        hld=win32gui.FindWindow(None, self.processName)
        print(hld)
        return hld

"""""entry"""""
if __name__ == '__main__':
    appPath='C:\eastmoney\swc8\EmTrade\EmTrade.exe PC_Free'
    appManager = AppRunManager(appPath)
    appManager.setForegroundWindow()

