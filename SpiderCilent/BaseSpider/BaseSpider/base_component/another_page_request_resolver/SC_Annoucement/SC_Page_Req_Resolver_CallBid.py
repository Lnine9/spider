from urllib.parse import parse_qs
import json
from scrapy import FormRequest
import requests

from BaseSpider.base_component.RequestResolver import RequestResolver


class SC_Page_Req_Resolver_CallBid(RequestResolver):
    """翻页请求解析器"""

    """
    允许自定义代码
    """

    def general_param(self) -> dict:
        # 必须在子方法中进行父方法调用
        super().general_param()

        # 以下为自定义代码
        gen_param = {}
        url = 'http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=recommendBulletinList&rp=25&page={pageindex}&moreType=provincebuyBulletinMore&channelCode=shiji_cggg'.format(pageindex = self.page_num)
        body = {}
        call_back = self.req_attr.call_back,
        method = 'GET',

        gen_param['url'] = url
        gen_param['body'] = ""
        gen_param['call_back'] = call_back
        gen_param['method'] = method


        return gen_param

    def create_request(self) -> FormRequest:
        # 必须在子方法中进行父方法调用
        super().create_request()



        '''
        以下为允许自定义方法

        '''

        if isinstance(self.url,tuple):
            self.url = self.general_param()["url"]

        request = FormRequest(
            self.url,
            callback=self.m_parse,
            method=self.method,
            formdata=None,
            dont_filter=self.dont_filter,
        )

        return request

    def m_parse(self, response):
        pass
