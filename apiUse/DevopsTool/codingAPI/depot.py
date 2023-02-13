#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   depot.py
@Time    :   2023/02/02 17:23:20
@Author  :   Xinbo Zhang
@Version :   1.0
@Contact :   xinbo.zhang@anker-in.com
@Description : Coding 代码仓库API
'''

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "../"))

from publicComponent.logs import logger
from publicComponent.httpRequest import https_request
from settings import GET, POST, EXCEPTION_CODE
from settings import CODING_HOST


# 查询仓库推送设置
def describeDepotPushSetting(token, depot_path):
    url = "/open-api?Action=DescribeDepotPushSetting"   
    data = {
        "Action": "DescribeDepotPushSetting",
        "DepotPath": depot_path
    }
    header = {"Authorization": "token {coding_token}".format(coding_token=token) }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=header, fields=data,urltype="HTTP")
    if status not in range(200, 300):
        logger.error("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    return result["Response"]["Data"]


# 查询仓库规范详情
def describeDepotSpecDetail(token, depot_path):
    url = "/open-api?Action=DescribeDepotSpecDetail"   
    data = {
        "Action": "DescribeDepotSpecDetail",
        "DepotPath": depot_path
    }
    header = {"Authorization": "token {coding_token}".format(coding_token=token) }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=header, fields=data,urltype="HTTP")
    if status not in range(200, 300):
        logger.error("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    return result["Response"]["Detail"]


# 查询所有保护分支
def describeProtectedBranchs(token, depot_id):
    url = "/open-api?Action=DescribeProtectedBranchs"   
    data = {
        "Action": "DescribeProtectedBranchs",
        "DepotId": depot_id
    }
    header = {"Authorization": "token {coding_token}".format(coding_token=token) }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=header, fields=data,urltype="HTTP")
    if status not in range(200, 300):
        logger.error("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    return result["Response"]["ProtectedBranchs"]
