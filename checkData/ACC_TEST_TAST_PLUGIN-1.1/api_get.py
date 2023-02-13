'''
@Author: pengfei.wang
@Email: pengfei.wang@anker.com
@Date: 2022/11/4 7:37 下午
@Description:    Coding API
'''


# ! API开放能力文档 https://help.coding.net/openapi
import sys
import os

sys.path.append(os.path.join(os.getcwd(), "../"))

from settings import CODING_API_TOKEN, POST
from tools import https_request
CODING_HOST = "codingcorp.coding.anker-in.com"  # anker-coding.coding.net
HEADER = {"Authorization": "token " + CODING_API_TOKEN}
DEBUG = 0  # 0 正式环境  1 调试环境


# *********************************************  以下为coding项目角色或成员的相关API


def get_projectUserList(ProjectId=10522952):  # 查询coding的项目成员   10522952  a

    url = "/open-api?Action=DescribeProjectMembers"
    data = {
        "Action": "DescribeProjectMembers",
        "PageNumber": 1,
        "PageSize": 100,
        "ProjectId": ProjectId
    }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=HEADER, fields=data, urltype="HTTP")
    if status not in range(200, 300):
        print("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    return result['Response']['Data']['ProjectMembers']


def get_UserInfo(projectUserList, keyword, keyValus, returnKey):  # 通过userlist返回的信息获取想要的信息，可以是name,id等,在用
    ProjectMembers = projectUserList
    for men in ProjectMembers:
        if men[keyword] == keyValus:  # keyword 可取值 Name，Id,GlobalKey等，参考api
            return men[returnKey]
    return None


def get_user_mail(projectUserList, roleName="ALL"):  # a
    roleList = []
    for men in projectUserList:
        uname = men['Name']
        if roleName == "ALL":
            roleList.append(men['Email'])
        else:
            role = men['Roles']
            for r in role:
                if r['RoleTypeName'] == roleName:
                    roleList.append(men['Email'])

    return roleList


def get_Role_User(projectUserList, roleType):  # 查询项目某一角色的成员ID清单  a
    roleList = []
    for men in projectUserList:
        role = men['Roles']
        for r in role:
            if r['RoleTypeName'] == roleType:
                roleList.append(men['Id'])
    return roleList


def get_meb_UserId(projectUserList, username):  # 查询项目某一角色的成员ID清单  a
    for men in projectUserList:
        name = men['Name']
        if name == username:
            return men['Id']
    return 0

def get_user_email_byname(projectUserList, username):  # 查询项目某一角色的成员ID清单  a
    for men in projectUserList:
        name = men['Name']
        if name == username:
            return men['Email']
    return ""

# *********************************************  以下为coding项目或事项相关的API


def get_projectIssueTypeList(ProjectName):  # 获取项目问题类型清单，在用，不要随便改动  a
    url = "/open-api?Action=DescribeProjectIssueTypeList"
    data = {
        "Action": "DescribeProjectIssueTypeList",
        "ProjectName": ProjectName
    }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=HEADER, fields=data, urltype="HTTP")
    if status not in range(200, 300):
        print("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    return result['Response']['IssueTypes']


def get_projectIssueTypeID(IssueTypesList, issueTypeName):  # 获取项目某一问题类型的ID，在用，不要随便改动  a
    for type in IssueTypesList:
        if type['Name'] == issueTypeName:
            return type['Id'], type['IssueType']
    return None, None


def get_ProjectIssueFieldList(ProjectName, IssueTypeValue,
                              IssueType="IssueType"):  # a获取项目里字段ID，全局字段在项目里应用ID会变,可以取值issueType,也可以取值issueTypeID
    url = "/open-api?Action=DescribeProjectIssueFieldList"
    data = {
        "Action": "DescribeProjectIssueFieldList",
        "ProjectName": ProjectName,
        IssueType: IssueTypeValue  # IssueType 取值 IssueType或IssueTypeId
    }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=HEADER, fields=data, urltype="HTTP")
    if status not in range(200, 300):
        print("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))

    return result['Response']['ProjectIssueFieldList']


def get_ProjectIssueFieldID(IssueFieldList, fieldName, ifOption=None, optionValue=None):  # a
    if ifOption == None:
        for issueField in IssueFieldList:
            if issueField['IssueField']['Name'] == fieldName:
                return issueField['IssueFieldId']

        return None
    else:
        for issueField in IssueFieldList:
            if issueField['IssueField']['Name'] == fieldName:
                options = issueField['IssueField']['Options']
                if len(options) != 0:
                    for op in options:
                        if op['Title'] == optionValue:
                            return issueField['IssueField']['Id'], str(op['Value'])  # 字段ID和选择项ID

                else:
                    return None, None


# *********************************************  以下为coding项目相关API
def get_projectID_by_name(ProjectName):
    url = "/open-api?Action=DescribeProjectByName"
    data = {
        "Action": "DescribeProjectByName",
        "ProjectName": ProjectName
    }
    status, result = https_request(CODING_HOST, url, methods=POST, headers=HEADER, fields=data, urltype="HTTP")
    if status not in range(200, 300):
        print("Request ERROR: {code}|{result}".format(code=status, result=result))
        raise Exception("Request ERROR: {code}|{result}".format(code=status, result=result))
    return result['Response']['Project']['Id']
