# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 13:13:27 2017

@author: chen
"""
import os,sys

vnpy2to3_cmd_test="\"C:/Program Files/Python36/Tools/scripts/2to3.py\" -w \"./vnpy/vnpy/event/eventType.py\""
vnpy2to3="\"C:/Program Files/Python36/Tools/scripts/2to3.py\" -w "
vnpyPath="./vnpy/vnpy"
py_suffix = ".py"
bak_suffix = ".py.bak"

def walk_dir(dir,fileinfo,topdown=True):
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            if name.endswith(py_suffix):
                print(os.path.join(name))
                fileinfo.write(os.path.join(root,name) + '\n')
                #vnpy2to3 -w os.path.join(root,name)
                #os.system(vnpy2to3 + '-w' + os.path.join(root,name))
                t_f = os.popen (vnpy2to3 + "\"" + os.path.join(root,name) + "\"")
                print(t_f.read())
            else:
                #print(os.path.join(name))
                pass


def delete_bak_file(dir,fileinfo,topdown=True):
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            if name.endswith(bak_suffix):
                print(os.path.join(root,name))
                #os.remove(os.path.join(root,name))

            else:
                #print(os.path.join(name))
                pass



# 直接运行脚本可以进行测试
if __name__ == '__main__':

    fileinfo = open('list.txt','w')
    walk_dir(vnpyPath,fileinfo)
    #t_f = os.popen (vnpy2to3_cmd_test)
    #t_f = os.popen (vnpy2to3 + "\"./vnpy/vnpy/event/eventType.py\"")   #test ok
    #t_f = os.popen (vnpy2to3 + "\"" + "./vnpy/vnpy/event/eventType.py" + "\"")   #test ok
    #print(t_f.read())
    #os.system(vnpy2to3 + '-w' + "./vnpy/vnpy/event/eventEngine.py")


    #delete_bak_file(vnpyPath,fileinfo)