#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   project.py
@Time    :   2023/02/02 14:21:19
@Author  :   Xinbo Zhang
@Version :   1.0
@Contact :   xinbo.zhang@anker-in.com
@Description : Coding 项目信息API
'''


import sys
import os

sys.path.append(os.path.join(os.getcwd(), "../"))

from publicComponent.logs import logger
from publicComponent.httpRequest import https_request
from codingAPI.format import RepoBasicInfo
from settings import GET, POST, EXCEPTION_CODE
from settings import CODING_HOST


# 获取项目下所有仓库信息列表
def describeProjectDepotInfoList(token, project_id):
    url = "/open-api?Action=DescribeProjectDepotInfoList"   
    data = {
        "Action": "DescribeProjectDepotInfoList",
        "ProjectId": project_id
    }
    header = {"Authorization": "token {coding_token}".format(coding_token=token) }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=header, fields=data,urltype="HTTP")
    if status not in range(200, 300):
        logger.error("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    data = result["Response"]["DepotData"]["Depots"]
    if not data:  # 项目下查询不到仓库信息
        return []
    depots = []
    for item in data:
        repo_basic_info = RepoBasicInfo(item["Id"], item["Name"], item["HttpsUrl"], item["SshUrl"], item["WebUrl"], item["VcsType"])
        depots.append(repo_basic_info)
    return depots
