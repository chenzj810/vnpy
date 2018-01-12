# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 10:25:30 2017

@author: chen
"""


import urllib
#import cookielib
import http.cookiejar
import time

## 这段代码是用于解决中文报错的问题
#reload(sys)
#sys.setdefaultencoding("utf8")
#####################################################
#

class Login(object):


    #----------------------------------------------------------------------
    def __init__(self):
        self.name = '540800288762'
        self.passwprd = '123456'
        self.captcha = ''
        self.validatekey = '94783938-d9c3-4219-a013-5d828e469353'
        self.filename = 'cookie.txt'

        # 将cookies绑定到一个opener cookie由cookielib自动管理
        #self.cookie = http.cookiejar.CookieJar()

        #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
        self.cookie = http.cookiejar.MozillaCookieJar(self.filename)

        self.cookiehand = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.cookiehand)
        urllib.request.install_opener(self.opener)


        self.timestamp =str(int(time.time()*1000))


    #----------------------------------------------------------------------
    def get_timstamp(self):
        timestamp =int(int(time.time()*1000))
        print(str(timestamp))
        return str(timestamp)



    #----------------------------------------------------------------------
    def get_Login_YZM(self):
        '''获取验证码'''


        self.randNumber = '0.6698980878585289'
        # 验证码地址
        self.captchaUrl = "https://jy.xzsec.com/Login/YZM?randNum=%s" % self.randNumber
        print(self.captchaUrl)

        # 用opener访问验证码地址,获取cookie
        response = self.opener.open(self.captchaUrl)
        result = response.read()
        print(response)
        print (result)


        # 保存验证码到本地
        local = open('e:/image.jpg', 'wb')
        local.write(result)
        local.close()

        # 保存验证码到本地
        self.captcha = input('输入验证码： ')
        print(self.captcha)


    #----------------------------------------------------------------------
    def post_Login_Authentication(self):
        '''登录网站'''

        #和post地址
        self.postLoginUrl = "https://jy.xzsec.com/Login/Authentication?validatekey="

        # 根据抓包信息 构造表单
        postData = {
        'userId': '540800288762',
        'password': '810523',
        'randNumber': self.randNumber,
        'identifyCode': self.captcha,
        'duration': '30',
        'authCode': '',
        'type': 'Z'
        }


        # 根据抓包信息 构造headers
        headers = {
        'Host': "jy.xzsec.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://jy.xzsec.com/Login?el=1&clear=1',
        'Connection': 'keep-alive',
        }

        # 生成post数据 ?key1=value1&key2=value2的形式
        data = urllib.parse.urlencode(postData).encode('utf-8')

        # 构造request请求
        request = urllib.request.Request(self.postLoginUrl, data, headers)

        try:
            response = self.opener.open(request)

            # 读取返回值
            #result = response.read().decode('gb2312')
            page = response.read().decode('utf-8')

            # 打印登录后的页面
            print ('response read:', page)

            # Make sure we are logged in, check the returned page content
            if page.find('\"Status\":0') ==-1:
                print ('Login failed')
                return False
            else:
                print ('Login succeeded!')

                #保存cookie到cookie.txt中
                self.cookie.save(ignore_discard=True, ignore_expires=True)
                return True



        except urllib.request.HTTPError:
            print (urllib.HTTPError)
            return False


    #----------------------------------------------------------------------
    def post_Login_CheckZjzh(self):
        '''登录网站后check，通过抓包分析, 密码输入错误时有次消息，密码输入正确是没有抓到该包'''

        #和post地址
        self.postCheckUrl = "https://jy.xzsec.com/Login/CheckZjzh?%s" % self.timestamp
        print (self.postCheckUrl)

        # 根据抓包信息 构造表单
        postData = {
        'zjzh': '540800288762'
        }


        # 根据抓包信息 构造headers
        headers = {
        'Host': "jy.xzsec.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://jy.xzsec.com/Login?el=1&clear=1',
        'Connection': 'keep-alive',
        }

        # 生成post数据 ?key1=value1&key2=value2的形式
        data = urllib.parse.urlencode(postData).encode('utf-8')

        # 构造request请求
        request = urllib.request.Request(self.postCheckUrl, data, headers)

        try:
            response = self.opener.open(request)

            # 读取返回值
            #result = response.read().decode('gb2312')
            page = response.read().decode('utf-8')

            # 打印登录后的页面
            print ('response read:', page)

            # Make sure we are logged in, check the returned page content
            if page.find('\"Status\":0') ==-1:
                print ('Login failed')
                return False
            else:
                print ('Login succeeded!')

                #保存cookie到cookie.txt中
                self.cookie.save(ignore_discard=True, ignore_expires=True)
                return True



        except urllib.request.HTTPError:
            print (urllib.HTTPError)
            return False




    #----------------------------------------------------------------------
    def get_Trade_Buy(self):
        '''登录网站后获取买卖页面的内容'''


        self.getTradeBuyUrl = "https://jy.xzsec.com/Trade/Buy"
        print (self.getTradeBuyUrl)

        # 用opener访问验证码地址,获取cookie
        response = self.opener.open(self.getTradeBuyUrl)
        result = response.read()
        print(response)
        print (result)

    #----------------------------------------------------------------------
    def get_Trade_PosPartial(self):
        '''登录网站后获取买卖页面的内容'''


        self.getTradeBuyUrl = "https://jy.xzsec.com/Js/Trade/PosPartial.js?v=2017080301"
        print (self.getTradeBuyUrl)

        # 用opener访问验证码地址,获取cookie
        response = self.opener.open(self.getTradeBuyUrl)
        result = response.read()
        print(response)
        print (result)


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

        #和post 买单地址
        self.postBuyUrl = "https://jy.xzsec.com/Trade/SubmitTrade?validatekey=%s" % self.validatekey

        # 根据抓包信息 构造表单
        postBuyData = {
        'stockCode': stockCode,
        'price': price,
        'amount': amount,
        'tradeType': 'B',   #现价买入
        'zqmc': name
        }


        # 根据抓包信息 构造headers
        headers = {
        'Host': "jy.xzsec.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://jy.xzsec.com/Trade/Buy',
        'Connection': 'keep-alive',
        }

        # 生成post数据 ?key1=value1&key2=value2的形式
        data = urllib.parse.urlencode(postBuyData).encode('utf-8')

        # 构造request请求
        request = urllib.request.Request(self.postBuyUrl, data, headers)

        try:
            response = self.opener.open(request)

            # 读取返回值
            #result = response.read().decode('gb2312')
            page = response.read().decode('utf-8')

            # 打印登录后的页面
            print ('response read:', page)

            # Make sure we are buy, check the returned page content
            if page.find('\"Status\":0') ==-1:
                print ('Buy failed')
                return False
            else:
                print ('Buy succeeded!')
                return True



        except urllib.request.HTTPError:
            print (urllib.HTTPError)
            return False


    #get 卖出页面
    #'tradeType': 'S'  现价卖出
    #'tradeType': '0f'  对手方最优价格申报
    #'tradeType': '0g'  本方最优价格申报
    #'tradeType': '0h'  即使申报剩余撤销申报
    #'tradeType': '0i'  最优五档即使申报剩余撤销申报
    #'tradeType': '0j'  全额成交或撤销申报
    #----------------------------------------------------------------------
    def sendSellOrder(self, stockCode, price, amount, name):
        '''发送买单'''

        #和post 买单地址
        self.postBuyUrl = "https://jy.xzsec.com/Trade/SubmitTrade?validatekey=%s" % self.validatekey

        # 根据抓包信息 构造表单
        postBuyData = {
        'stockCode': stockCode,
        'price': price,
        'amount': amount,
        'tradeType': 'S',   #现价卖出
        'zqmc': name
        }


        # 根据抓包信息 构造headers
        headers = {
        'Host': "jy.xzsec.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://jy.xzsec.com/Trade/Buy',
        'Connection': 'keep-alive',
        }

        # 生成post数据 ?key1=value1&key2=value2的形式
        data = urllib.parse.urlencode(postBuyData).encode('utf-8')

        # 构造request请求
        request = urllib.request.Request(self.postBuyUrl, data, headers)

        try:
            response = self.opener.open(request)

            # 读取返回值
            #result = response.read().decode('gb2312')
            page = response.read().decode('utf-8')

            # 打印登录后的页面
            print (page)

            # Make sure we are logged in, check the returned page content
            if page.find('\"Status\":0') != -1:
                print ('Buy succeeded!')
                return True
            elif page.find('\"Status\":-2') != -1:
                print ('Login timeout')
                return False
            else:
                print ('Buy failed!')
                return False



        except urllib.request.HTTPError:
            print (urllib.HTTPError)
            return False


    #----------------------------------------------------------------------
    def getAssertInfo(self):
        '''获取资产信息'''

        #和post 资产信息地址
        self.postAssertUrl = "https://jy.xzsec.com/Com/GetAssets?validatekey=%s" % self.validatekey

        # 根据抓包信息 构造表单
        # 无表单信息

        # 根据抓包信息 构造headers
        headers = {
        'Host': "jy.xzsec.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://jy.xzsec.com/Trade/Buy',
        'Connection': 'keep-alive',
        }


        # 构造request请求
        request = urllib.request.Request(self.postAssertUrl, headers=headers)

        try:
            response = self.opener.open(request)

            # 读取返回值
            #result = response.read().decode('gb2312')
            page = response.read().decode('utf-8')

            # 打印登录后的页面
            print (page)

        except urllib.request.HTTPError:
            print (urllib.HTTPError)

    #----------------------------------------------------------------------
    def getMyStockInfo(self):
        '''获取账户中股票信息'''

        #和post 资产信息地址
        self.postMyStockInfoUrl = "https://jy.xzsec.com/Search/GetStockList?validatekey=%s" % self.validatekey

        # 根据抓包信息 构造表单
        postStockData = {
        'qqhs': '1000',
        'dwc': ''
        }

        # 根据抓包信息 构造headers
        headers = {
        'Host': "jy.xzsec.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://jy.xzsec.com/Trade/Buy',
        'Connection': 'keep-alive',
        }


        # 构造request请求
        request = urllib.request.Request(self.postMyStockInfoUrl, postStockData, headers)

        try:
            response = self.opener.open(request)

            # 读取返回值
            #result = response.read().decode('gb2312')
            page = response.read().decode('utf-8')

            # 打印登录后的页面
            print (page)

        except urllib.request.HTTPError:
            print (urllib.HTTPError)



#----------------------------------------------------------------------
#    抓包信息, 密码或验证码错误的情形
#    获取验证码：userlogin.login_YZM(), GET
#    登陆，携带用户名，密码：userlogin.login_Authentication(), POST
#    检查：userlogin.login_CheckZjzh(), POST


#----------------------------------------------------------------------
#    抓包信息, 密码或验证码正确的情形
#    获取验证码：userlogin.login_YZM(), GET
#    登陆，携带用户名，密码：userlogin.login_Authentication(), POST
#    检查：userlogin.login_CheckZjzh(), POST
def testLogin(userlogin):
    '''测试登陆'''

    userlogin.get_Login_YZM()
    userlogin.post_Login_Authentication()
    userlogin.post_Login_CheckZjzh()

    print(userlogin.cookie)
    for item in userlogin.cookie:
        print ('Name = '+item.name)
        print ('Value = '+item.value)

def testSendBuyOrder(userlogin):
    '''测试下买单'''

    #从文件中读取cookie内容到变量
    userlogin.cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    print(userlogin.cookie)

    #userlogin.cookiehand = urllib.request.HTTPCookieProcessor(userlogin.cookie)
    #userlogin.opener = urllib.request.build_opener(userlogin.cookiehand)
    userlogin.sendBuyOrder('002500', '11.36', '100', '山西证券')

def testLoginAndBuy(userlogin):
    '''测试登陆并且下买单'''

    userlogin.get_Login_YZM()

    result = userlogin.post_Login_Authentication()
    if result==True:
        userlogin.sendBuyOrder('002500', '11.36', '100', '山西证券')

def testLoginAndGetBuyPage(userlogin):
    '''测试登陆并且下买单'''

    userlogin.get_Login_YZM()

    result = userlogin.post_Login_Authentication()
    if result==True:
        userlogin.get_Trade_Buy()
        userlogin.get_Trade_PosPartial()
        userlogin.sendBuyOrder('002500', '11.36', '100', '山西证券')


if __name__ == '__main__':

    userlogin = Login()
    #testLogin(userlogin)
    #testLoginAndGetBuyPage(userlogin)
    testSendBuyOrder(userlogin)