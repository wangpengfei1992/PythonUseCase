#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   user.py
@Time    :   2023/02/02 10:48:34
@Author  :   Xinbo Zhang
@Version :   1.0
@Contact :   xinbo.zhang@anker-in.com
@Description : Coding 用户信息API
'''

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "../"))

from publicComponent.logs import logger
from publicComponent.httpRequest import https_request
from codingAPI.format import UserInfo, ProjectInfo
from settings import GET, POST, EXCEPTION_CODE
from settings import CODING_HOST



# 获取 Coding 用户信息
def describeCodingCurrentUser(token):
    url = "/open-api?Action=DescribeCodingCurrentUser"   
    data = {
        "Action": "DescribeCodingCurrentUser"
    }
    header = {"Authorization": "token {coding_token}".format(coding_token=token) }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=header, fields=data,urltype="HTTP")
    if status not in range(200, 300):
        logger.error("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    user_info = UserInfo(result["Response"]["User"]["Id"], result["Response"]["User"]["Name"], result["Response"]["User"]["Email"], result["Response"]["User"]["Phone"])
    return user_info


# 获取 Coding 成员所在的项目列表
def describeUserProjects(token, user_id):
    url = "/open-api?Action=DescribeUserProjects"   
    data = {
        "Action": "DescribeUserProjects",
        "UserId": user_id
    }
    header = {"Authorization": "token {coding_token}".format(coding_token=token) }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=header, fields=data,urltype="HTTP")
    if status not in range(200, 300):
        logger.error("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    data = result["Response"]["ProjectList"]
    if not data: # 用户没有添加到任何项目
        return []
    projects = []
    for item in data:
        project_info = ProjectInfo(item["Id"], item["Name"], item["DisplayName"], item["Description"], item["UserOwnerId"])
        projects.append(project_info)
    return projects
