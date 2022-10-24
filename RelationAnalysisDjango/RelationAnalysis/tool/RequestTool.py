import requests


class HttpRequest(object):
    """不记录任何的请求方法"""

    @classmethod
    def request(cls, method, url, data=None, headers=None):  # 这里是要传入的参数，请求方法、接口地址、传参、头文件
        method = method.upper()  # 这里将传入的请求方法统一大写，然后进行判断采用什么方法
        if method == 'POST':
            return requests.post(url=url, data=data, headers=headers)
        elif method == 'GET':
            return requests.get(url=url, params=data, headers=headers)


class HttpSession(object):
    __http = None
    """记录Session的方法"""

    def __init__(self):
        self.session = requests.session()  # 初始化一个保存session的方法

    def request(self, url, data=None, headers=None):
        return self.session.post(url=url, data=data, headers=headers)

    def post(self, url, data=None, headers=None):
        return self.request(url, data, headers)

    def close(self):
        """断开session连接的方法"""
        self.session.close()

    @classmethod
    def get_http_session(cls):
        if not cls.__http:
            cls.__http = HttpSession()
        return cls.__http


def obj2Dict(arg):
    """
    将指定类型对象转化为json格式
    :param arg:
    :return:
    """
    if isinstance(arg, list):
        for index, item in enumerate(arg):
            arg[index] = obj2Dict(item)
        return arg
    elif isinstance(arg, dict):
        return arg
    elif isinstance(arg, object):
        arg_dict = arg.__dict__
        if arg_dict['_sa_instance_state'] is not None:
            arg_dict.pop('_sa_instance_state')
        return arg_dict
