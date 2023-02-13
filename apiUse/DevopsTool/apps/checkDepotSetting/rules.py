#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   rules.py
@Time    :   2023/02/03 18:12:01
@Author  :   Xinbo Zhang
@Version :   1.0
@Contact :   xinbo.zhang@anker-in.com
@Description : 代码仓库配置检查规则
'''

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "../.."))

from codingAPI.depot import describeDepotPushSetting, describeDepotSpecDetail, describeProtectedBranchs


def check_rules(token, project_name, depot_id, depot_name):
    errors = []
    depot_path = "codingcorp/{project_name}/{depot_name}".format(project_name=project_name, depot_name=depot_name)
    try:
        # 推送配置
        push_setting = describeDepotPushSetting(token, depot_path)
        if "CheckCommitAuthor" in push_setting and not push_setting["CheckCommitAuthor"]:  # 未检查 Git 提交的提交者 (Committer) 和提交作者 (Author) 必须是已验证的邮箱
            errors.append('推送设置：未检查 Git 提交的提交者 (Committer) 和提交作者 (Author) 必须是已验证的邮箱')
        # if "DenyForcePush" in push_setting and not push_setting["DenyForcePush"]:  # 未检查禁止强制推送 (Force Push)
        #     errors.append('推送设置：未检查 禁止强制推送 (Force Push)')
        if "CommitMessageMustMatchRegex" in push_setting and not push_setting["CommitMessageMustMatchRegex"]:  # 未检查 开启 Git 提交信息的格式校验
            errors.append('推送设置：未开启 Git 提交信息的格式校验')
        # 仓库规范
        spec_detail = describeDepotSpecDetail(token, depot_path)
        if "AllowPushWildRef" in spec_detail and spec_detail["AllowPushWildRef"]:  # 未禁止允许创建规定分支类型以外的分支
            errors.append('仓库规范：未禁止允许创建规定分支类型以外的分支')
        if "UseExistingSolution" in spec_detail and not spec_detail["UseExistingSolution"]:  # 未使用已有的仓库规范方案
            errors.append('仓库规范：未使用已有的仓库规范方案')
        # 保护分支
        protected_branch = describeProtectedBranchs(token, depot_id)
        if "ProtectedBranchs" in protected_branch and not protected_branch["ProtectedBranchs"]:  # 未设置保护分支
            errors.append('保护分支：未设置保护分支')
    except Exception:
        return errors
    return errors
