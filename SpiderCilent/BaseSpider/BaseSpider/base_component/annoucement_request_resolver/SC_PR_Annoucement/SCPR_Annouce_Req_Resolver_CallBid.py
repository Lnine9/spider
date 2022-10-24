from scrapy import FormRequest
import scrapy

# 初始网页请求
from BaseSpider.base_component.RequestResolver import RequestResolver
from BaseSpider.tool.SpecialFormRequest import SpecialForm


class SCPR_Annouce_Req_Resolver_CallBid(RequestResolver):
    """
    公告请求解析器
    """

    def general_param(self) -> dict:
        # 必须加载父类方法
        super().general_param()

        gen_param = {'url': self.url, 'call_back': self.call_back}
        return gen_param

    def create_request(self):
        # 必须加载父类方法
        super().create_request()

        request = SpecialForm(
            self.url,
            callback=self.m_parse,
            formdata=self.body,
            method=self.method,
            dont_filter=self.dont_filter,
            meta=self.meta,
            special=True
        )
        print(type(request))
        return request

    def m_parse(self, response):
        pass
