# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging

from component.wpf_log import loger, configLog
from component.wpf_tool import unLock, System_spec


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def logM(msg):
    loger.error(msg)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    configLog(True)
    print_hi('PyCharm')
    logM("测试打印")
    for i in range(10):
        logM(str(i))

    # unLock("res/12345.pdf")
    System_spec()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
