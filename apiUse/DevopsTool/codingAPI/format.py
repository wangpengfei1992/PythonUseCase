#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   format.py
@Time    :   2023/02/02 11:38:58
@Author  :   Xinbo Zhang
@Version :   1.0
@Contact :   xinbo.zhang@anker-in.com
@Description : Coding API 数据保存格式定义
'''

import collections


# 用户信息存储格式
UserInfo = collections.namedtuple("UserInfo", ["id", "name", "email", "phone"])

# 项目信息存储格式
ProjectInfo = collections.namedtuple("ProjectInfo", ["id", "name", "display_name", "description", "owner_id"])

# 代码仓库基础信息
RepoBasicInfo = collections.namedtuple("RepoBasicInfo", ["id", "name", "https_url", "ssh_url", "web_url", "vsc_type"])