#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   logs.py
@Time    :   2023/02/02 10:19:28
@Author  :   Xinbo Zhang
@Version :   1.0
@Contact :   xinbo.zhang@anker-in.com
@Description : 日志打印方法
'''

import logging

logging.basicConfig(
    format="[%(asctime)s %(levelname)s/%(filename)s %(funcName)s:%(lineno)d::%(process)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger()

# 打开log打印，设置打印级别
logger.setLevel("DEBUG")
