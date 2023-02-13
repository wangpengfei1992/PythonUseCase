#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   emails.py
@Time    :   2023/02/03 14:01:58
@Author  :   Xinbo Zhang
@Version :   1.0
@Contact :   xinbo.zhang@anker-in.com
@Description : 邮件发送工具
'''

import sys
import os
import traceback
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sys.path.append(os.path.join(os.getcwd(), "../"))

from publicComponent.logs import logger
from settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL


def get_template_html_content(template_path, template_data):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        template = Template(content)
        html = template.render(**template_data)
    return html


def toAndCcEmail(subject, template_path, template_data={}, toEmail=[], ccEmail=[]):
    try:
        msg = get_template_html_content(template_path, template_data)
        message = MIMEText(msg, 'html', 'utf-8')
        message['From'] = Header('Pengfei.Wang', 'utf-8')
        message['To'] = Header(",".join(toEmail), 'utf-8')
        message['Cc'] = Header(",".join(ccEmail), 'utf-8')
        message['Subject'] = subject
        smtp = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        smtp.sendmail(DEFAULT_FROM_EMAIL, toEmail + ccEmail, message.as_bytes())
        logger.info('邮件已发送！')
    except smtplib.SMTPException:
        logger.error("邮件发送失败")
        logger.error(traceback.format_exc())
        sys.exit(1)


def sendmail(subject, template_path, template_data={}, receiver=[]):
    try:
        msg = get_template_html_content(template_path, template_data)
        message = MIMEText(msg, 'html', 'utf-8')
        message['From'] = Header('Pengfei.Wang', 'utf-8')
        message['To'] = Header('pengfei.wang@anker-in.com', 'utf-8')
        message['Cc'] = Header('pengfei.wang@anker-in.com', 'utf-8')
        message['Subject'] = subject
        smtp = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        smtp.sendmail(DEFAULT_FROM_EMAIL, receiver, message.as_bytes())
        logger.info('邮件已发送！')
    except smtplib.SMTPException:
        logger.error("邮件发送失败")
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    # 发送测试邮件
    template_path = os.path.join(os.getcwd(), '../htmls/test.html')
    sendmail("测试邮件", template_path, template_data={"input": "Devops"}, receiver=["pengfei.wang@anker-in.com"])
