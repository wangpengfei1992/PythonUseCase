#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   settings.py
@Time    :   2023/01/31 18:04:38
@Author  :   Xinbo Zhang
@Version :   1.0
@Contact :   xinbo.zhang@anker-in.com
@Description : 全局配置文件
'''

# HTTP请求方式枚举
GET = "GET"
POST = "POST"
DELETE = "DELETE"
PATCH = "PATCH"
PUT = "PUT"

# 邮件发送配置
EMAIL_HOST = 'smtp.feishu.cn'
EMAIL_FAIL_SILENTLY = False 
EMAIL_USE_SSL = True 
EMAIL_PORT = 465
EMAIL_HOST_USER = 'pdp-acc-coding@anker-in.com'
EMAIL_HOST_PASSWORD = '------------'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# 异常处理代码
EXCEPTION_CODE = 500

# Coding地址
CODING_HOST = "codingcorp.coding.anker-in.com"    #anker-coding.coding.net

# Coding API Header格式
CODING_HEADER = {"Authorization": "token {coding_token}" }

# Coding API token 测试使用
CODING_API_TOKEN="--------------------"

