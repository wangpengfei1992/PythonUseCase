# 学习链接： https://www.liaoxuefeng.com/wiki/1016959663602400/1016959735620448
# Demo:https://github.com/seeways/PythonDemo

# http://c.biancheng.net/view/2241.html
# thread类依赖 pip install threading
# json第三方库：Demjson ，需要安装 http://deron.meranda.us/python/demjson/install
import datetime
import time

import _thread
import json

from component.wpf_log import configLog, loger
from component.wpf_singleton import MySingleton

isFinish = 1


def thead_test(name, delay):
    count = 0
    print(f'00000')
    while count < 3:
        time.sleep(1)
        configLog(True)
        loger.error("%s,%s", name, count)
        count += 1

    global isFinish
    isFinish = 0


def json_test():
    data1 = [{"a": 1, "c": 3, "b": 2, "e": 5, "d": 4}]
    # json对象转字符串
    jsonStr = json.dumps(data1)
    loger.error(jsonStr)
    strData = '{"a":1,"b":2,"c":3,"d":4,"e":5}'
    # 字符串转json对象
    dataJson = json.loads(strData)
    loger.error(dataJson)


def practise():
    for i in range(1, 3):
        for j in range(1, 3):
            if i != j:
                loger.error("%s,%s", i, j)


if __name__ == '__main__':
    print(f'入口执行函数')
    json_test()
    practise()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    loger.error("%s", time.localtime())
    singleton = MySingleton()
    singleton.myMethon()
    # # 创建多个线程，执行顺序与创建顺序无关
    # _thread.start_new_thread(thead_test, ("thread1", 1,))
    # _thread.start_new_thread(thead_test, ("thread2", 2,))
    # # sleep是为了保护子线程不退出
    # # time.sleep(100)
    # while isFinish:
    #     print(f'主程序循环1s')
    #     time.sleep(1)

    print(f'主程序结束')
