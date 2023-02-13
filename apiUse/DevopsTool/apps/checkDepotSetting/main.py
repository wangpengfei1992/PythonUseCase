#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2023/02/03 15:07:49
@Author  :   Xinbo Zhang
@Version :   1.0
@Contact :   xinbo.zhang@anker-in.com
@Description : 检查用户Coding下代码仓库配置
'''

import sys
import os
import argparse
import datetime

sys.path.append(os.path.join(os.getcwd(), "../.."))

from publicComponent.logs import logger
from publicComponent.emails import sendmail, toAndCcEmail
from codingAPI.user import describeCodingCurrentUser, describeUserProjects
from codingAPI.project import describeProjectDepotInfoList
from apps.checkDepotSetting.rules import check_rules


def get_arguments():
    parse = argparse.ArgumentParser(description="Check Depot Settings")
    parse.add_argument("--token", help='coding token', required=True)
    parse.add_argument("--toEmails", help='接收 emails', required=True)
    parse.add_argument("--ccEmails", help='抄送 emails', required=True)
    return parse.parse_args()


def check_one_project(token, project_id, project_name):
    depots = describeProjectDepotInfoList(token, project_id)
    if not depots:
        return []
    result = []
    for depot in depots:
        data = {
            "name": depot.name,
            "web_url": depot.web_url,
            "errors": check_rules(token, project_name, depot.id, depot.name)
        }
        result.append(data)
    return result


def analysis_data(info):
    now = datetime.datetime.now()
    project_num = len(info.keys())
    depot_num, error_depot = 0, 0
    for project, depots in info.items():
        depot_num = depot_num + len(depots)
        for item in depots:
            if "errors" in item.keys() and len(item["errors"]) > 0:
                error_depot = error_depot + 1
    data = {
        "project_num": project_num,
        "depot_num": depot_num,
        "error_depot": error_depot,
        "info": info,
        "checkDate": now.strftime("%Y-%m-%d %H:%M:%S")
    }
    return data


def start(args):
    user_info = describeCodingCurrentUser(args.token)
    projects = describeUserProjects(args.token, user_info.id)
    if not projects:
        logger.info("未加入Coding项目")
        return
    info = {}
    for project in projects:
        info[project.name] = check_one_project(args.token, project.id, project.name)
    data = analysis_data(info)
    template_path = os.path.join(os.getcwd(), '..\\..\\htmls/depot_check.html')
    to_list = args.toEmails.split(',')
    cc_list = args.ccEmails.split(',')
    # sendmail("Coding 代码仓库配置规范性检查", template_path, template_data=data, receiver=["xinbo.zhang@anker-in.com"]+to_list)
    toAndCcEmail("ACC Coding代码仓库配置规范性检查结果周知", template_path, template_data=data,
                 toEmail=["pengfei.wang@anker-in.com"] + to_list, ccEmail=cc_list)


if __name__ == '__main__':
    args = get_arguments()
    start(args)
    logger.info("====>>> Finished at {now}".format(now=datetime.datetime.now()))
