from urllib.parse import parse_qs

import requests
from scrapy import FormRequest, Selector

from ...RequestResolver import RequestResolver

class XNZF(RequestResolver):
    """
    允许自定义代码
    """
    total_page = None


    def general_param(self) -> dict:
        # 必须在子方法中进行父方法调用
        super().general_param()

        # 以下为自定义代码
        gen_param = {}

        if self.req_attr.page_num == 1:
            url = 'https://jhc.swupl.edu.cn/tzgg/index.htm'
        else:
            url = 'https://jhc.swupl.edu.cn/tzgg/index' + str(self.req_attr.page_num - 1) + '.htm',
        call_back = self.req_attr.call_back,
        method = 'GET',

        gen_param['url'] = url
        gen_param['call_back'] = call_back
        gen_param['method'] = method

        return gen_param

    def create_request(self) -> FormRequest:
        # 必须在子方法中进行父方法调用
        super().create_request()

        '''
        以下为允许自定义方法

        '''
        # 将字符串转换为字典
        params = parse_qs(self.body)
        result = {key: params[key][0] for key in params}

        request = FormRequest(
            self.url,
            callback=self.m_parse,
            method=self.method,
            formdata=result,
            dont_filter=self.dont_filter
        )
        return request

    def m_parse(self, response):
        pass







