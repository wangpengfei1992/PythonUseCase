"""
coding:utf-8
@Software:PyCharm
@Time:2023/2/14 14:59
@Author:王鹏飞
"""
from email.header import Header
from email.mime.text import MIMEText
import smtplib

# 邮件发送配置
EMAIL_HOST = 'smtp.feishu.cn'
EMAIL_FAIL_SILENTLY = False
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'pengfei@qq.com'
EMAIL_HOST_PASSWORD = '-----'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# subject：发送的主题(显示在标题)  content: 发送的内容  receiver:接收人
def sendmail(subject, content, receiver=[]):
    try:
        msg = content
        message = MIMEText(msg, 'html', 'utf-8')
        message['From'] = Header('Pengfei.Wang', 'utf-8')
        # 发送给
        message['To'] = Header('pengfei.wang@anker-in.com', 'utf-8')
        # 抄送给
        message['Cc'] = Header('pengfei.wang@anker-in.com', 'utf-8')
        message['Subject'] = subject
        smtp = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        smtp.sendmail(DEFAULT_FROM_EMAIL, receiver, message.as_bytes())
        print(f'邮件已发送！')
    except smtplib.SMTPException:
        print(f'邮件发送失败')
