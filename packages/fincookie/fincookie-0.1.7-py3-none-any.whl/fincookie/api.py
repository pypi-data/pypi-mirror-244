import requests
import socket

cloud_api = f"http://10.55.3.250/cookieService/"
local_api = "http://hive.finchina.local/api/hwy/cookieService/"
dev_api = "http://10.17.214.105/"

MODE = 'USER'


def set_dev(dev: bool = True):
    global MODE
    if dev is True:
        MODE = 'DEVELOPER'
    else:
        MODE = "USER"


def get_cookies(appid, get_last=0, block_timeout=0, url=None, url_timeout=None, script=None,
                wait_for=None, wait_timeout=None, selector=None, state=None, action=None, type_string=None,
                renew_interval=None) -> dict:
    ip = socket.gethostbyname(socket.gethostname())
    api = cloud_api if ip[:5] == '10.55' else dev_api if MODE == 'DEVELOPER' else local_api
    data = {k: v for k, v in locals().items() if isinstance(v, (int, str))}
    json_data = requests.post(api, data=data).json()
    return json_data


def get_logs(appid: str = None, date_from: str = None, request_id: str = None):
    params = "?"
    params += f'appid={appid}&' if appid else ''
    params += f'from={date_from}&' if date_from else ''
    params += f'request={request_id}' if request_id else ''
    ip = socket.gethostbyname(socket.gethostname())
    api = cloud_api if ip[:5] == '10.55' else dev_api if MODE == 'DEVELOPER' else local_api
    api = api + 'get_logs' + params
    res = requests.get(api)
    return res.text.replace('<br>', '\n')


def get_loads():
    ip = socket.gethostbyname(socket.gethostname())
    api = cloud_api if ip[:5] == '10.55' else dev_api if MODE == 'DEVELOPER' else local_api
    api = api + "get_loads"
    res = requests.get(api)
    return res.json()


def cookie_format(cookies: dict or str):
    if isinstance(cookies, dict):
        return "; ".join([f"{key}={value}" for key, value in cookies.items()])
    else:
        return dict([(item.split("=", 1)[0].strip(), item.split("=", 1)[1].strip()) for item in cookies.split(";")])


def headers_format(headers: dict or str):
    if isinstance(headers, dict):
        return "\n".join([f"{key}: {value}" for key, value in headers.items()])
    else:
        return dict([(item.split(":", 1)[0].strip(), item.split(":", 1)[1].strip()) for item in headers.split("\n")])


def proxy_format(proxy: str):
    return {"http": proxy, "https": proxy}
