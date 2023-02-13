#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   httpRequest.py
@Time    :   2023/02/02 10:17:35
@Author  :   Xinbo Zhang
@Version :   1.0
@Contact :   xinbo.zhang@anker-in.com
@Description : HTTP/HTTPS 请求方法
'''

import sys
import os
import traceback
import urllib3
import json
from http import client
# 取消ssl证书
import ssl

sys.path.append(os.path.join(os.getcwd(), "../"))

from publicComponent.logs import logger
from settings import GET, POST, DELETE, PATCH, PUT, EXCEPTION_CODE

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()


def https_request(host, url, methods=POST, fields={}, headers=None, urltype="HTTPS"): 
    if urltype=="HTTPS":
        conn = client.HTTPSConnection(host)
    else:
        conn = client.HTTPConnection(host)
    params = json.dumps(fields)
    conn.request(methods, url, params, headers=headers)
    resp = conn.getresponse()
    try:
        result = json.loads(resp.read().decode("UTF-8"), strict=False)
        status = resp.code
        #logger.info(result)
        conn.close()
        return status, result
    except Exception:
        status = resp.code
        conn.close()
        return status, "Http Error!"


class BaseHttpRequest(object):

    def __init__(self):
        pass

    def base_send_request(self, req_url, request_method=None, headers=None, fields=None):
        http = urllib3.PoolManager(cert_reqs="CERT_NONE", timeout=120)
        try:
            resp = http.request(request_method, req_url, fields=fields, headers=headers, retries=5)
        except Exception:
            err = "{err}".format(err=traceback.format_exc())
            logger.error(err)
            return EXCEPTION_CODE, err
        status = resp.status
        result = resp.data.decode() if status in range(200, 300) else None
        resp.release_conn()
        return status, result


class BaseAuthHttpRequest(BaseHttpRequest):

    def __init__(self, req_url, username, password, request_method=None, headers=None, fields=None):
        self.req_url, self.username, self.password, self.request_method = req_url, username, password, request_method
        if not headers:
            self.headers = urllib3.util.make_headers(
                basic_auth="{username}:{password}".format(username=self.username, password=self.password)
            )
        else:
            self.headers = headers
        logger.debug(self.headers)
        super(BaseHttpRequest, self).__init__()

    def send_request(self):
        try:
            status, result = self.base_send_request(self.req_url, self.request_method, self.headers)
            return status, result
        except Exception:
            err = "{err}".format(err=traceback.format_exc())
            logger.error(err)
            return EXCEPTION_CODE, err
