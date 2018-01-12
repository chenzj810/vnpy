# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 17:17:05 2017

@author: chen
"""
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import serverFromString
from twisted.web import http
import os, time
import argparse
import subprocess
from multiprocessing import Process, Queue, Pool
import multiprocessing


########################################################################
class CommonClass(object):

    dataPath = "/opt/data/"    # 指明被遍历的文件夹
    dictFile = '/opt/data/rockyou.txt'    # 字典路径
    bind = ''
    port = 80
    taskList = []
    capfile_lock = None   # cap file lock
    crackfile_lock = None  # crack file lock

    # 静态方法，
    @staticmethod
    def loopupKey(rootdir, filename):

        for root, dirs, files in os.walk(rootdir, True):
            for name in files:
                tmpfile = os.path.join(root, name)
                #print(name, tmpfile, filename)
                if name == filename:
                    print('crack file is exist, ', filename)

                    #直接打开一个文件，如果文件不存在则创建文件
                    with open(tmpfile, 'r') as f:
                        key = f.read(100)
                        #print('key:', key)
                        return key

            for name in dirs:
                #print(os.path.join(name))
                pass
        return None

    @staticmethod
    def getPathFileName(rootdir, bassid, ssid):

        path = rootdir + time.strftime("%Y-%m", time.localtime()) + '/'
        path = path.strip()
        if not os.path.exists(path):
            # 如果不存在则创建目录
            print (rootdir," not exist")
            # 创建目录操作函数
            os.makedirs(path)

        #pcap文件, 去掉特殊字符：
        filename = bassid.replace(':', "", 6) + ssid
        capfile = filename + '.cap'
        crackfile = filename + '.crack'
        print('generate path:', path, 'filename:', filename, 'capfile:', capfile, 'crackfile:', crackfile)
        return path, filename, capfile, crackfile


    @staticmethod
    def find_key(crack_result):
        if crack_result is None:
            return None

        begin = crack_result.find('KEY FOUND! [ ')
        offset = len('KEY FOUND! [ ')
        if begin > 0:
            end = crack_result.find(' ]', begin)
            #print(type(begin), type(end), type(crack_result))
            return crack_result[begin + offset:end]
        else:
            return None

    @staticmethod
    def queue_put(q, value):
        q.put(value)

    @staticmethod
    def queue_get(q):
        return q.get()

    '''
    @classmethod
    def cap_write(cls, file, value):
        cls.capfile_lock.acquire()
        print('capfile_lock acquire')
        with open(file, 'wb') as fp:
            fp.write(value)
            #fp.close()
        print('capfile_lock release')
        cls.capfile_lock.release()

    @classmethod
    def crack_write(cls, file, value):
        cls.crackfile_lock.acquire()
        print('crackfile_lock acquire')
        with open(file, 'w') as fp:
            fp.write(value)
            #fp.close()
        print('crackfile_lock release')
        cls.crackfile_lock.release()
    '''

    @staticmethod
    def cap_write(file, value, lock):
        lock.acquire()
        #print('capfile_lock acquire')
        try:
            fp = open(file, 'wb')
            fp.write(value)
        finally:
            fp.close()

        #print('capfile_lock release')
        lock.release()

    @staticmethod
    def crack_write(file, value, lock):
        lock.acquire()
        #print('crackfile_lock acquire')
        try:
            fp = open(file, 'w')
            fp.write(value)
        finally:
            fp.close()
        #print('crackfile_lock release')
        lock.release()

    @staticmethod
    def crack_delete(file, lock):
        lock.acquire()
        try:
            os.remove(file)
        except:
            pass
        lock.release()


########################################################################
class MyRequestHandler(http.Request):
    # 队列
    q = None


    def process(self):
        if isinstance(self.method, str):
            method = self.method
            url = self.uri
        else:
            method = self.method.decode('utf-8')
            url = self.uri.decode('utf-8')

        #print(self.args)
        print(method, url)
        if url == '/data/crack' and method == 'POST':
            self.dataCrackProcess()
        else:
            print('url unknow')
            self.setResponseCode(http.NOT_FOUND)
            self.finish()


    # post 处理
    def dataCrackProcess(self):
        # 数据参数解析到字典中
        #print('type:', 'bssid'.encode(), {'bssid':'11:22', 'ssid':'ddd'})
        formdata = {}
        for (key, value) in self.args.items():
            #print(type(key), type(value[0]))
            if isinstance(key, str):
                print('key:', key, 'value:', value)
            else:
                k = key.decode('utf-8')

                # file 以二进制方式保存
                if k == 'file':
                    v = value[0]
                else:
                    v = value[0].decode('utf-8')

                print('key:', k, 'value:', v, 'type:', v.__class__.__name__)
                formdata[k] = v

        # 回应报文设置
        self.setHeader('Content-Type', 'text/plain')

        # 报文有效性检查
        if not 'bssid' in formdata or not 'ssid' in formdata:
            retmsg = "{\"ret_code\":\"-1\",\"ret_msg\":\"报文无法识别\"}"
            retmsg = retmsg.encode('utf-8')
            print(retmsg)
            self.setResponseCode(http.OK)
            self.write(retmsg)
            self.finish()
            return

        if self.q.qsize() > 10:
            retmsg = "{\"ret_code\":\"-2\",\"ret_msg\":\"服务器破解忙\"}"
            retmsg = retmsg.encode('utf-8')
            print(retmsg)
            self.setResponseCode(http.OK)
            self.write(retmsg)
            self.finish()
            return


        path, filename, capfile, crackfile = CommonClass.getPathFileName(CommonClass.dataPath, formdata['bssid'], formdata['ssid'])

        # 如果带了文件，就直接覆盖
        if 'file' in formdata:
            self.q.put(formdata)
            retmsg = "{\"ret_code\":\"1\",\"ret_msg\":\"开始破解\"}"
            retmsg = retmsg.encode('utf-8')
            print(retmsg)
            self.setResponseCode(http.OK)
            self.write(retmsg)
            self.finish()
            return

        # 查询流程
        # 查找该文件是否破解过，如果破解过，直接读取密码
        ret = CommonClass.loopupKey(CommonClass.dataPath, crackfile)
        if ret is not None:
            retmsg = "{\"ret_code\":\"0\",\"ret_msg\":\"%s\"}" % (ret)
            retmsg = retmsg.encode('utf-8')
            print(retmsg)
            self.setResponseCode(http.OK)
            self.write(retmsg)
            self.finish()
            return

        # 没有找到crack文件，说明没有破解
        #self.q.put(formdata)
        retmsg = "{\"ret_code\":\"2\",\"ret_msg\":\"正在破解中\"}"
        retmsg = retmsg.encode('utf-8')
        self.setResponseCode(http.OK)
        self.write(retmsg)
        self.finish()
        return





########################################################################
def crack_task_handle(q, capfile_lock, crackfile_lock):
    while True:
        # 直接读取，空的时候阻塞cpu
        postdata = q.get(True)
        print('PID:', os.getpid(), 'read queue:', postdata)

        path, filename, capfile, crackfile = CommonClass.getPathFileName(CommonClass.dataPath, postdata['bssid'], postdata['ssid'])
        print('capfile:', capfile, 'crackfile:', crackfile)
        #print(CommonClass.__dict__)

        cap_fullname = path + capfile
        crack_fullname = path + crackfile

        # 如果带了文件，就直接覆盖
        if 'file' in postdata:
            # 删除.crack文件
            CommonClass.crack_delete(crack_fullname, crackfile_lock)

            #直接打开一个文件，如果文件不存在则创建文件, 二进制
            CommonClass.cap_write(cap_fullname, postdata['file'], capfile_lock)
            print('cover cap file, start decode:', cap_fullname)


        # 如果没有a 参数，默认为2
        if not 'a' in postdata:
            postdata['a'] = 2

        ## 破解密码
        cap_fullname = path + capfile
        cmd = "/usr/local/bin/aircrack-ng -a %s -e %s -b %s -w %s %s" %(postdata['a'], postdata['ssid'], postdata['bssid'],
                                                                        CommonClass.dictFile, cap_fullname)
        #cmd = "aircrack-ng -a 2 -e watch_dog -b FC:83:06:80:19:44 -w data/rockyou.txt data/czb6.cap"

        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # 阻塞父进程, 返回值是元组
        cmdResult = p.communicate()
        cmdResult = cmdResult[0].decode('utf-8')
        #print('aircrack cmd result:', cmdResult)

        # 破解的密码
        key = CommonClass.find_key(cmdResult)
        if key is not None:
            CommonClass.crack_write(crack_fullname, key, crackfile_lock)
            print ('decode finish, found key:', key, 'save key to file:', crackfile)
        elif cmdResult.find('No matching network') >= 0:
            print('No matching network')
        else:
            pass
            print('decode finish, dont found key, quit')

########################################################################

'''
class MyHTTP(http.HTTPChannel): #继承高级API http.HTTPChannel
    requestFactory=MyRequestHandler

class MyHTTPFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return MyHTTP()
'''
########################################################################
def main():
    """Test the HTTP request handler class.

    This runs an HTTP server on port 8000 (or the port argument).

    """

    # 破解密码子进程， 启动
    '''
    #q = Queue(300)

    p1 = Process(target=crack_proc, args=(q,))
    p1.start()


    p2 = Process(target=crack_proc, args=(q,))
    p2.start()
    '''

    #使用进程池中使用队列则要使用multiprocess的Manager类
    q = multiprocessing.Manager().Queue(300)
    CommonClass.capfile_lock = multiprocessing.Manager().Lock()
    CommonClass.crackfile_lock = multiprocessing.Manager().Lock()

    pool = Pool()
    for i in range(multiprocessing.cpu_count()):
        print("hello %d" %(i))
        pool.apply_async(crack_task_handle, args=(q, CommonClass.capfile_lock, CommonClass.crackfile_lock))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去

    pool.close()
    #pool.join()
    print(CommonClass.__dict__)

    #主进程
    serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
    print(serve_message.format(host=CommonClass.bind, port=CommonClass.port))


    #client = MongoClient("localhost", 27017)
    #db=client.crackpkg
    #collection = db['000797']
    #print(collection.name)




    factory = http.HTTPFactory()
    factory.protocol = http.HTTPChannel

    MyRequestHandler.q = q
    http.HTTPChannel.requestFactory = MyRequestHandler

    serverFromString(reactor,'tcp:' + str(CommonClass.port)).listen(factory)


    #reactor.listenTCP(80, MyHTTPFactory())
    reactor.run()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--bind', '-b', default='', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')

    parser.add_argument('--port', action='store',
                        default=80, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 80]')

    parser.add_argument('--dict', action='store',
                        default='rockyou.txt', type=str,
                        nargs='?',
                        help='The dictionary file [default: /opt/data]')

    parser.add_argument('--data', action='store',
                        default='/opt/data/', type=str,
                        nargs='?',
                        help='The path of dta [default: /opt/data/]')


    args = parser.parse_args()

    print('中文测试')
    print(args)

    # 参数解析
    if args.dict:
        CommonClass.dictFile = args.data + args.dict
    if args.data:
        CommonClass.dataPath = args.data
    if args.bind:
        CommonClass.bind = args.bind
    if args.port:
        CommonClass.port = args.port



    main()
    #main(port=80, bind='192.168.99.30')
