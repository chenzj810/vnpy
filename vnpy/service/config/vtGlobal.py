# encoding: UTF-8

"""
通过VT_setting.json加载全局配置
"""

import os
import traceback
import json


globalSetting = {}      # 全局配置字典


settingFileName = "VT_setting.json"
path = os.path.abspath(os.path.dirname(__file__))
print(path)
settingFileName = os.path.join(path, settingFileName)

try:
    f = open(settingFileName, 'rb')
    globalSetting = json.load(f)
    print(globalSetting)
except:
    traceback.print_exc()

