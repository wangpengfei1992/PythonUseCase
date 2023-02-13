'''
@Author: pengfei.wang
@Email: pengfei.wang@anker.com
@Date: 2022/11/4 7:37 下午
@Description:
参考：https://coding.net/help/docs/ci/plugins/customize/format.html
https://coding.net/help/openapi#6656f7e04229a4da4db4967ecb1b16b8
'''

# coding:utf-8
import re
import sys
import argparse
import os
import smtplib
import subprocess
from email.header import Header
from email.mime.text import MIMEText

from api_get import get_projectIssueTypeID, get_projectIssueTypeList, get_ProjectIssueFieldList, get_projectUserList, \
    get_Role_User, get_projectID_by_name, get_ProjectIssueFieldID, get_user_mail, get_meb_UserId, get_user_email_byname
from settings import CODING_API_TOKEN, MAIL_SENDER, MAIL_HOST, MAIL_PASSWD, POST
from tools import https_request

CODING_HOST = "codingcorp.coding.anker-in.com"
HEADER = {"Authorization": "token " + CODING_API_TOKEN}
DEBUG = 0  # 0 正式环境  1 调试环境


def get_arguments():
    parse = argparse.ArgumentParser(description="Coding Version")
    parse.add_argument("--packageVersion", help='packageVersion', required=True)
    parse.add_argument("--buildEnv", help='buildEnv', required=True)
    parse.add_argument("--buildNo", help='buildNo', required=True)
    parse.add_argument("--selftestResultLink", help='selftestResultLink', required=True)
    parse.add_argument("--testDescription", help='testDescription', required=True)
    parse.add_argument("--plat", help='plat', required=True)
    parse.add_argument("--packageLink", help='packageLink')
    parse.add_argument("--versionPhase", help='versionPhase', required=True)
    parse.add_argument("--testOwner", help='testOwner', required=True)
    parse.add_argument("--testSubmitter", help='testSubmitter')
    parse.add_argument("--productName", help='productName', required=True)
    parse.add_argument("--firmwareVersion", help='firmwareVersion', required=True)
    parse.add_argument("--relationVersion", help='relationVersion', required=True)

    return parse.parse_args()


def create_version_task(buildEnv,projectName, versionName, IterationID, plat,AssignedToId, IssueTypeId, issueType, Description,
                        CustomFieldValues):
    #【提测】【pdp_aw_app】【Android】V2.4.0
    url = "/open-api?Action=CreateIssue"
    data = {
        "Action": "CreateIssue",
        "ProjectName": projectName,
        "Type": issueType,
        "IssueTypeId": IssueTypeId,
        "Name": "【提测" + buildEnv + "】【" + projectName + "】【" + plat + "】"+ versionName,
        "Priority": "1",
        "AssigneeId": AssignedToId,
        "IterationCode": IterationID,
        "Description": Description,
        "CustomFieldValues": CustomFieldValues
    }
    print(projectName, versionName, IterationID, AssignedToId, IssueTypeId, issueType)
    status, result = https_request(CODING_HOST, url, methods=POST, headers=HEADER, fields=data, urltype="HTTP")
    if status not in range(200, 300):
        print("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    print(result)


def create_test_plan_task(projectName, versionName, IterationID, AssignedToId):
    url = CODING_HOST + "/open-api?Action=CreateTestRun"
    data = {
        "Action": "CreateTestRun",
        "IncludeAll": True,
        "Name": versionName + "测试计划",
        "ProjectName": projectName,
        "IterationId": IterationID,
        "AssignedToId": AssignedToId
    }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=HEADER, fields=data, urltype="HTTP")
    if status not in range(200, 300):
        print("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))


def get_iteration_List(projectName, IterationName):
    url = "/open-api?Action=DescribeIterationList"
    data = {
        "Action": "DescribeIterationList",
        "ProjectName": projectName,
        "keywords": IterationName
    }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=HEADER, fields=data, urltype="HTTP")
    # status, result = https_post(CODING_HOST, url,  headers=HEADER, fields=data)

    if status not in range(200, 300):
        print("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    return result['Response']['Data']['List']


def get_iteration_id(iterationList, IterationName):
    for it in iterationList:
        if it['Name'] == IterationName:
            return it['Code']
    return None


def issueType(projectName):
    url = "/open-api?Action=DescribeProjectIssueTypeList"
    data = {
        "Action": "DescribeProjectIssueTypeList",
        "ProjectName": projectName,
    }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=HEADER, fields=data, urltype="HTTP")
    if status not in range(200, 300):
        print("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    print(result)


def sendemail(Subject, des, senderList, ccList):
    senderStrList = ",".join(senderList)
    ccStrList = ",".join(ccList)
    message = MIMEText(des, 'plain', 'utf-8')
    message['From'] = Header("acc devops", 'utf-8')
    message['Subject'] = Header(Subject, 'utf-8')
    message['To'] = Header(senderStrList, 'utf-8')
    message['Cc'] = Header(ccStrList, 'utf-8')

    try:

        smtpObj = smtplib.SMTP('smtp.feishu.cn')
        smtpObj.connect('smtp.feishu.cn', '587')

        smtpObj.ehlo()
        smtpObj.starttls()

        smtpObj.login(MAIL_SENDER, MAIL_PASSWD)

        # smtpObj = smtplib.SMTP()
        #
        # smtpObj.connect(MAIL_HOST, 587)  # 25 为 SMTP 端口号
        # smtpObj.ehlo()
        # smtpObj.starttls()
        # smtpObj.login(MAIL_SENDER, MAIL_PASSWD)
        smtpObj.sendmail(MAIL_SENDER, senderList + ccList, message.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(e)
        print("Error: 无法发送邮件")


if __name__ == '__main__':
    args = get_arguments()
    IterationName = args.packageVersion
    buildEnv = args.buildEnv
    buildNo = args.buildNo
    selftestResultLink = args.selftestResultLink
    testDescription = args.testDescription
    plat = args.plat
    packageLink = args.packageLink
    versionPhase = args.versionPhase
    testOwner = args.testOwner
    testSubmitter = args.testSubmitter
    productName = args.productName
    firmwareVersion = args.firmwareVersion
    relationVersion = args.relationVersion
    subprocess.call("env", shell=True)



    if testSubmitter is None or testSubmitter == 0:
        testSubmitter = os.getenv('TRIGGER_USER_NAME')
    print("触发方式", os.getenv('CCI_TRIGGER_METHOD'))
    print("触发者用户名", os.getenv('TRIGGER_USER_NAME'))
    print("触发者邮箱", os.getenv('TRIGGER_USER_EMAIL'))



    # IterationName = "test_V1.0.0.1"
    # buildNo = "2"
    # selftestResultLink = "www.baidu.com"
    # testDescription = "我要测试插件"
    # plat = "iOS"
    # packageLink = "wwww.fpt.com"
    # versionPhase = "量产前版本"
    # testOwner = "yiyi.chen"
    # testSubmitter = "pengfei.wang"
    # productName = "pdp_acc"
    # firmwareVersion = "3.0"

    iteration_id = get_iteration_id(get_iteration_List(productName, IterationName),
                                    IterationName)  # 获取迭代编号，提测任务归属迭代
    # SUB_VERSION_STR = get_subVersion_to_jira(projectName, IterationName)
    # gujian_url = get_gujian_url(project, IterationName)

    userAll_mail = get_user_mail(get_projectUserList(get_projectID_by_name(productName)), "ALL")
    testerL = get_user_mail(get_projectUserList(get_projectID_by_name(productName)), "Anker-测试主责")
    tester_mail = list(
        set(testerL + get_user_mail(get_projectUserList(get_projectID_by_name(productName)), "Anker-测试工程师")))
    cc_mail = list(set(userAll_mail) - set(tester_mail))

    # 处理更新内容
    string1 = testDescription
    # print(string1)
    string1 = str(string1)
    set_res = set(re.findall(r'\\[a-z]', string1))
    list_res = list(set_res)
    print(list_res)
    for target in list_res:
        string_tmple = re.compile(repr(target)[1:-1])
        string1 = string_tmple.sub(repr(target)[2:-1], string1)
    # print(string1)

    descriptionContent = ""
    if plat == "Cloud":
        platVersion = "APP版本："+relationVersion
        descriptionContent = '''【{buildEnv}提测通知】项目{productName} {platName} {version}\n---------制品所属平台：{ofPlatform}---------
                · 所属迭代：{version}
                · 版本阶段：{versionStage}
                · 提测人：{triggerName}
                · 测试对接人：{testerL}
                一、版本信息\n· 版本号：{buildNo}\n· 固件版本：{firmwareV}\n· {platV}\n二、自测试报告\n \000 {selftest_url} \n三、ReleaseNote\n{releaseNote}
                    '''.format(buildEnv=buildEnv, productName=productName, platName=plat, version=IterationName, buildNo=buildNo,
                               selftest_url=selftestResultLink,
                               releaseNote=string1, ofPlatform=plat, versionStage=versionPhase,
                               triggerName=testSubmitter, testerL=testOwner, firmwareV=firmwareVersion,
                               platV=platVersion
                               )
    else:
        platVersion = "后台版本：" + relationVersion
        descriptionContent = '''【{buildEnv}提测通知】项目{productName} {platName} {version}\n---------制品所属平台：{ofPlatform}---------
                · 所属迭代：{version}
                · 版本阶段：{versionStage}
                · 提测人：{triggerName}
                · 测试对接人：{testerL}
                一、版本信息\n· 版本号：{buildNo}\n· 固件版本：{firmwareV}\n· {platV}\n二、自测试报告\n \000 {selftest_url} \n三、测试包下载路径\n \000 {gujian_url}\n四、ReleaseNote\n{releaseNote}
                    '''.format(buildEnv=buildEnv, productName=productName, platName=plat, version=IterationName, buildNo=buildNo,
                               selftest_url=selftestResultLink, gujian_url=packageLink,
                               releaseNote=string1, ofPlatform=plat, versionStage=versionPhase,
                               triggerName=testSubmitter, testerL=testOwner, firmwareV=firmwareVersion,
                               platV=platVersion
                               )

    CustomFieldList = {
        "版本阶段": versionPhase,
        "提测任务所属平台": plat}

    IssueTypeId, issueTypeName = get_projectIssueTypeID(get_projectIssueTypeList(productName), "提测任务")
    IssueFieldList = get_ProjectIssueFieldList(productName, IssueTypeId, "IssueTypeId")
    CustomFieldListStr = []
    for c in CustomFieldList.keys():
        IssueFieldId, IssueFieldOptionId = get_ProjectIssueFieldID(IssueFieldList, c, True, CustomFieldList[c])
        str_cus = {
            "Id": IssueFieldId,
            "Content": IssueFieldOptionId
        }
        CustomFieldListStr.append(str_cus)

    print(descriptionContent)
    projectMebsers = get_projectUserList(get_projectID_by_name(productName))
    testOwnerId = get_meb_UserId(projectMebsers, testOwner)
    # rolelist = get_Role_User(tester_mail, "Anker-测试主责")
    # if testOwnerId == 0 and rolelist:
    #     testOwnerId = rolelist[0]

    create_version_task(buildEnv,productName, IterationName, iteration_id, plat,
                        testOwnerId,
                        # 分配处理人
                        IssueTypeId, issueTypeName, descriptionContent, CustomFieldListStr)

    # 发邮件
    subject_str = "项目{project} {version} {buildEnv}提测通知".format(project=productName, version=IterationName, buildEnv=buildEnv)
    # senduser=get_user_email_byname(projectMebsers,testSubmitter)
    sendemail(subject_str, descriptionContent, tester_mail, cc_mail)
