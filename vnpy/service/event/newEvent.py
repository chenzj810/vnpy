from __future__ import print_function

import pyuv
import signal
import socket
import ctypes


reader, writer = socket.socketpair()
reader.setblocking(False)
writer.setblocking(False)

def prepare_cb(handle):
    print("Inside prepare_cb")
    handle.close()

def excepthook(typ, val, tb):
    print("Inside excepthook")
    if typ is KeyboardInterrupt:
        prepare.stop()
        signal_checker.stop()

def worker_cb():
    for i in range(8):
        print("Inside worker_cb", i)
    count = 0
    while count < 5:
       print (count, " 小于 5")
       #count = count + 1

def worker_done(handle):
    print("Inside worker_done")
    #handle.close()

def async_cb(handle):
    print("Inside prepare_cb")
    #print(pyuv.util.cpu_info())
    handle.close()
    #self.stop()

loop = pyuv.Loop.default_loop()


myasync = pyuv.Async(loop, async_cb)
myasync.send()


#loop.queue_work = worker_cb
loop.excepthook = excepthook
loop.queue_work(worker_cb, worker_done)
#print(req)
'''
loop.excepthook = excepthook
prepare = pyuv.Prepare(loop)
prepare.start(prepare_cb)

signal.set_wakeup_fd(writer.fileno())
signal_checker = pyuv.util.SignalChecker(loop, reader.fileno())
signal_checker.start()
'''

loop.run()
