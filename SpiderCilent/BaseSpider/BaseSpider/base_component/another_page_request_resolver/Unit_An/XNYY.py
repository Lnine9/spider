from urllib.parse import parse_qs

import requests
from scrapy import FormRequest, Selector

from ...RequestResolver import RequestResolver

class XNYY(RequestResolver):
    """
    允许自定义代码
    """
    total_page = None


    def general_param(self) -> dict:
        # 必须在子方法中进行父方法调用
        super().general_param()

        # 以下为自定义代码
        gen_param = {}

        total_page = self.total_page
        if not total_page:
            resp = Selector(text=requests.get('http://www.xnyy.cn/zbcg.htm').text)
            total_page = int(resp.xpath("//span[@class='p_no'][last()]/a/text()").extract_first())
            self.total_page = total_page

        if self.req_attr.page_num == 1:
            url = 'http://www.xnyy.cn/zbcg.htm'
        else:
            url = 'http://www.xnyy.cn/zbcg/' + str(total_page - self.req_attr.page_num + 1) + '.htm',
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







