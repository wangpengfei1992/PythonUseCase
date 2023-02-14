import json
from http import client
# 取消ssl证书
import ssl
import urllib3
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()
# HTTP请求方式枚举
GET = "GET"
POST = "POST"
DELETE = "DELETE"
PATCH = "PATCH"
PUT = "PUT"

def https_request(host, url, methods='', fields={}, headers=None, urltype="HTTPS"):
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