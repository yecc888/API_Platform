__author__ = 'yecc'
__date__ = '2020/5/3 10:52'

import requests, os, sys, logging, time
from requests.exceptions import ConnectTimeout, HTTPError, InvalidURL, \
    InvalidHeader, ConnectionError
import json, simplejson
from datetime import datetime
import django
import threading

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + '../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "API_PLATFORM.settings")
django.setup()
from .models import ApiResponse, CustomParameters
from .serializers import ApiResponseSerializer
from .utils import doDatas, get_customParas
from base.models import EnvManager
from base.serializers import EnvSerializer

logger = logging.getLogger('django')


def send(test_data):
    """
    快速测试
    :param test_data:
    :return:
    """
    url = test_data['url']
    method = test_data['method']
    protoclo = test_data['protocol']
    env_id = test_data['env']
    headers = {}
    # get_env(test_data)
    for k1, v1 in enumerate(test_data['headers']):
        if v1['name'] is not '' or v1['raw'] is not '':
            if v1['name'] is not '' and v1['raw'] is '':
                key = v1['name']
                value = v1['value']
                # headers.update({key: value})
                if "${__" in value:
                    c_key = get_customParas(value)
                    key_value = CustomParameters.objects.get(key=c_key).value
                    headers.update({key: key_value})
                else:
                    headers.update({key: value})
            else:
                if isinstance(v1['raw'], dict):
                    headers.update(v1['raw'])
                else:
                    headers.update(eval(v1['raw']))
    payload = {}
    for k, v in enumerate(test_data['paramars']):
        if v['name'] is not '' or v['raw'] is not '':
            if v['name'] is not '' and v['raw'] is '':
                key = v['name']
                value = v['value']
                # 处理自定义变量
                if key == 'req' and "${__" in value:
                    req_raw = eval(value)
                    # req_raw = json.loads(value)
                    for raws_key, raws_value in req_raw.items():
                        if "${__" in str(raws_value):
                            c_key = get_customParas(raws_value)
                            key_value = CustomParameters.objects.get(key=c_key).value
                            req_raw.update({raws_key: key_value})
                    payload.update({key: json.dumps(req_raw)})
                    # continue
                elif "${__" in value and key != 'req':
                    c_key = get_customParas(value)
                    key_value = CustomParameters.objects.get(key=c_key).value
                    payload.update({key: key_value})
                else:
                    payload.update({key: value})
            else:
                if isinstance(v['raw'], dict):
                    payload.update(v['raw'])
                else:
                    raws = eval(v['raw'])  # 将字符串转换为dict
                    # 处理自定义参数
                    for raws_key, raws_value in raws.items():
                        if "${__" in str(raws_value):
                            c_key = get_customParas(raws_value)
                            key_value = CustomParameters.objects.get(key=c_key).value
                            raws.update({raws_key: key_value})
                    payload.update(raws)
    # form-data 类型数据
    if 'req' in payload.keys():
        urlencond_formdata(payload)

    if method.upper() == 'GET':
        return get(url=url, method=method, payload=payload,
                   headers=headers, test_data=test_data)
    elif method.upper() == 'POST':
        return post(url=url, method=method, payload=payload,
                    headers=headers, test_data=test_data)


def get(url, method, payload, headers, test_data):
    try:
        req = requests.request(url=url, method=method, params=payload,
                               headers=headers, timeout=3)
    except ConnectTimeout as ex:
        logger.error(ex)
        return req.raise_for_status(), {}, {ex}, {}
    except HTTPError as ex:
        logger.error(ex)
        return req.raise_for_status(), {}, {ex}, {}
    except InvalidURL as ex:
        logger.error(ex)
        return req.raise_for_status(), {}, {ex}, {}
    try:
        try:
            if test_data.get('id', ''):
                # 请求成功
                if req.status_code == requests.codes.ok and req.content:
                    try:
                        header = json.dumps(dict(req.headers))
                        result = json.dumps(req.json())
                        result_seriaziler = ApiResponseSerializer(data={"api": test_data['id'],
                                                                        "status_code": req.status_code,
                                                                        "response_header": header,
                                                                        "response_content": result,
                                                                        "response_time": int(
                                                                            req.elapsed.microseconds / 1000),
                                                                        "response_status": "success"}
                                                                  )
                        if result_seriaziler.is_valid():
                            result_seriaziler.save()
                    except Exception:
                        raise
                        # 请求失败
                elif str(req.status_code).startswith('4') or str(req.status_code).startswith('5'):
                    try:
                        header = json.dumps(dict(req.headers))
                        result = json.dumps(req.json())
                        result_seriaziler = ApiResponseSerializer(data={"api": test_data['id'],
                                                                        "status_code": req.status_code,
                                                                        "response_header": header,
                                                                        "response_content": result,
                                                                        "response_time": int(
                                                                            req.elapsed.microseconds / 1000),
                                                                        "response_status": "danger",
                                                                        }
                                                                  )
                        if result_seriaziler.is_valid():
                            result_seriaziler.save()
                    except Exception:
                        raise
            else:
                pass
        except Exception as ex:
            logger.error(ex)
            raise
        return req.status_code, req.headers, req.json(), req.elapsed.microseconds / 1000
    except json.decoder.JSONDecodeError:
        return req.status_code, req.headers, {req.content}, req.elapsed.microseconds / 1000
    except simplejson.errors.JSONDecodeError:
        return req.status_code, req.headers, {req.content}, req.elapsed.microseconds / 1000
    except Exception as ex:
        logger.exception('ERROR')
        logger.debug(str(ex))
        return req.status_code, req.headers, {}, {}


def post(url, method, payload, headers, test_data):
    if 'application/json' in headers.values():
        payload = json.dumps(payload)
    try:
        req = requests.request(url=url, method=method, data=payload,
                               headers=headers, timeout=3)
    except HTTPError as ex:
        logger.error(ex)
        return req.raise_for_status(), {}, {ex}, {}
    except InvalidURL:
        return req.raise_for_status(), {}, {}, {}
    except ConnectTimeout as ex:
        logger.error(ex)
        return req.raise_for_status(), {}, {ex}, {}
    except ConnectionError as ex:
        logger.error(ex)
        return {}, {}, {ex}, {}
    try:
        try:
            if test_data.get('id', ''):
                # 请求成功
                if req.status_code == requests.codes.ok and req.content:
                    try:
                        header = json.dumps(dict(req.headers))
                        result = json.dumps(req.json())
                        result_seriaziler = ApiResponseSerializer(data={"api": test_data['id'],
                                                                        "status_code": req.status_code,
                                                                        "response_header": header,
                                                                        "response_content": result,
                                                                        "response_time": int(
                                                                            req.elapsed.microseconds / 1000),
                                                                        "response_status": "success"}
                                                                  )
                        if result_seriaziler.is_valid():
                            result_seriaziler.save()
                    except Exception:
                        raise
                        # 请求失败
                elif str(req.status_code).startswith('4') or str(req.status_code).startswith('5'):
                    try:
                        header = json.dumps(dict(req.headers))
                        result = json.dumps(req.json())
                        result_seriaziler = ApiResponseSerializer(data={"api": test_data['id'],
                                                                        "status_code": req.status_code,
                                                                        "response_header": header,
                                                                        "response_content": result,
                                                                        "response_time": int(
                                                                            req.elapsed.microseconds / 1000),
                                                                        "response_status": "danger",
                                                                        }
                                                                  )
                        if result_seriaziler.is_valid():
                            result_seriaziler.save()
                    except Exception:
                        raise
            else:
                pass
        except Exception as ex:
            logger.error(ex)
            raise
        return req.status_code, req.headers, req.json(), req.elapsed.microseconds / 1000
    except json.decoder.JSONDecodeError:
        return req.status_code, req.headers, {req.content}, req.elapsed.microseconds / 1000
    except simplejson.errors.JSONDecodeError:
        return req.status_code, req.headers, {req.content}, req.elapsed.microseconds / 1000
    except Exception as ex:
        logger.exception('ERROR')
        logger.debug(str(ex))
        return req.status_code, req.headers, {}, {}


def urlencond_formdata(payload):
    """
    处理 application/x-www-form-urlencoded类型的数据
    :param payload:
    :return:
    """
    if 'v' not in payload:
        v = '2.0'
        payload.update({'v': v})
    else:
        v = payload.get('v', {})
    if 'ts' not in payload:
        ts = int(time.time())
        payload.update({"ts": ts})
    else:
        ts = payload.get('ts', {})
    if 'appid' not in payload:
        appid = 'dp1svA1gkNt8cQMkoIv7HmD1'
        payload.update({"appid": appid})
    else:
        appid = payload.get('appid', {})
    if 'appkey' not in payload:
        appkey = '4660e73cd9891459889f9362384acc39'
    else:
        appkey = payload.get('appkey', {})
        payload.pop('appkey')

    if 'sig' not in payload:
        data = payload.get('req', {})
        if isinstance(data, str):
            data = json.loads(data)
        sig = doDatas(data=data, appid=appid, appkey=appkey, v=v, ts=ts).sign_data
        payload.update({'sig': sig})


def get_env(test_data):
    """
    获取环境相关参数
    :param _id:
    :return:
    """
    _id = test_data['env']
    protocol = test_data['protocol']
    env = EnvManager.objects.filter(id=_id).values()[0]
    desc = env.get('desc')
    host = env.get('host')
    port = env.get('port')
    status = env.get('status')
    if status == 2:
        if 'http' not in host:
            if port:
                host = "http://" + host + ":" + port
            else:
                host = "http://" + host
        elif "https" not in host:
            if port:
                host = "https://" + host + ":" + port
            else:
                host = "https://" + host
        if desc:
            if "appid" in desc:
                pass

    print(env)


class MyThead(threading.Thread):
    """

    """

    def __init__(self):
        threading.Thread.__init__()

    def run(self):
        print(threading.Thread.name)


if __name__ == "__main__":
    url = 'https://www.baidu.com'
    method = 'GET'
    p = '"uuiui":787878\n"iiooi":"8888"'
    import string

    print(string.ascii_letters)
    headers = {'Content-Type': 'application/json'}
    if 'application/json' in headers:
        print(1)
