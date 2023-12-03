
import io
import os
import yaml
import hashlib
import socket
from typing import List
from loguru import logger
from urllib import parse

# 定义常量
CONFIGURATIONS = "configurations"
NOTIFICATION_ID = "notificationId"
NAMESPACE_NAME = "namespaceName"
RELEASE_KEY = "releaseKey"
CONTENT = "content"


# 对时间戳，uri，秘钥进行加签
def signature(timestamp, uri, secret):
    import hmac
    import base64
    string_to_sign = '' + timestamp + '\n' + uri
    hmac_code = hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha1).digest()
    return base64.b64encode(hmac_code).decode()


def url_encode_wrapper(params):
    return url_encode(params)


def no_key_cache_key(namespace, key):
    return "{}{}{}".format(namespace, len(namespace), key)


# 返回是否获取到的值，不存在则返回None
def get_value_from_dict(namespace_cache, key):
    if namespace_cache:
        kv_data = namespace_cache.get(CONFIGURATIONS)
        if kv_data is None:
            return None
        if key in kv_data:
            return kv_data[key]
        sub_keys = key.split(".")
        # 获取yaml格式的参数
        return get_value_in_yaml(kv_data, sub_keys)
    return None


def init_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        ip = s.getsockname()[0]
        logger.info("======IP:{}====", ip)
        return ip
    finally:
        s.close()


def get_value_in_yaml(kv_data, args: List):
    result_tmp = kv_data
    if len(args) < 0:
        return None
    for arg in args:
        if result_tmp is None:
            return None
        if arg in result_tmp:
            result_tmp = result_tmp[arg]
        else:
            return None
    return result_tmp


# 统一处理apollo查询的数据
def handle_resp_body(data):
    data = data[CONFIGURATIONS]
    # 解析yaml 格式
    if CONTENT in data and data[CONTENT] is not None:
        dataByes = data[CONTENT].encode('utf-8')
        f = io.BytesIO(dataByes)
        return yaml.load(stream=f, Loader=yaml.FullLoader)
    return data


def url_encode(params):
    return parse.urlencode(params)


def makedir_wrapper(path):
    os.makedirs(path, exist_ok=True)


# 默认文件缓存路径
def get_default_cache_file_path():
    return os.path.join("var", "data", "apollo", "cache")
