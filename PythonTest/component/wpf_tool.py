# 常用的工具
# 安装第三方库命令：pip install pikepdf

# 图片处理第三方piplow
import os

import pikepdf
from PIL import Image


# 方法1
def testImag():
    test_img = Image.open("../res/1.png")
    test_img.save("../res/2.png")


# pdf加解密

def unLock(path):
    pdf = pikepdf.open(path, allow_overwriting_input=True)
    pdf.save("res/5.pdf")
    pdf.close()


def unlock_file(file):
    # pdf = pikepdf.open("encrypt.pdf", password='your_password')
    pdf = pikepdf.open(file, allow_overwriting_input=True)
    # pdf.save('encrypt.pdf', encryption=pikepdf.Encryption(owner="your_password", user="your_password", R=4))
    pdf.save(file)


def unlock_directory(folder='./'):
    os.chdir(folder)
    filelist = os.listdir()
    for file in filelist:
        if os.path.splitext(file)[1] == '.pdf':
            unlock_file(file)


# 电脑配置
import wmi



def System_spec():
    Pc = wmi.WMI()
    os_info = Pc.Win32_OperatingSystem()[0]
    processor = Pc.Win32_Processor()[0]
    Gpu = Pc.Win32_VideoController()[0]
    # os_name = os_info.Name.encode('utf-8').split(b'|')[0]
    os_name = os_info.Name
    ram = float(os_info.TotalVisibleMemorySize) / 1048576

    print(f'操作系统: {os_name}')
    print(f'CPU: {processor.Name}')
    print(f'内存: {ram} GB')
    print(f'显卡: {Gpu.Name}')

    print("\n计算机信息如上 ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑")

# 解压文件ZipFile

# Excel表操作：import pandas as pd

# 图像转换 import cv2

# 获取CPU温度
# from time import sleep
# from pyspectator.processor import Cpu


# 提取PDF表格
# 方法一：import camelot