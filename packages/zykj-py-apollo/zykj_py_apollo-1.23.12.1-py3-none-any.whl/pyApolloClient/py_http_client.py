
from loguru import logger

import urllib.request
from urllib.error import HTTPError


def http_request(url, timeout, headers={}):
    try:
        request = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(request, timeout=timeout)
        body = res.read().decode("utf-8")
        return res.code, body
    except HTTPError as e:
        if e.code == 304:
            logger.warning("http_request error,code is 304, maybe you should check secret")
            return 304, None
        logger.warning("http_request error,code is {}, msg is {}", e.code, e.msg)
        raise e

