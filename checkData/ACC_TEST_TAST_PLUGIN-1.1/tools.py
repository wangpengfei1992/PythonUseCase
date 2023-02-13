'''
@Author: pengfei.wang
@Email: pengfei.wang@anker.com
@Date: 2022/11/4 7:37 下午
@Description:        
'''
import json
from http import client




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


