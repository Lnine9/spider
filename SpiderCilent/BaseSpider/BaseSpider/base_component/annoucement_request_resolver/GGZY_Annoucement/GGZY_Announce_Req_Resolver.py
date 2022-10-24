
from scrapy import FormRequest

# 初始网页请求
from BaseSpider.base_component.RequestResolver import RequestResolver


class GGZY_Announce_Req_Resolver(RequestResolver):

    def general_param(self) -> dict:
        # 必须加载父类方法
        super().general_param()

        gen_param = {'url': self.url, 'call_back': self.call_back}
        return gen_param

    def create_request(self) -> FormRequest:
        # 必须加载父类方法
        super().create_request()

        request = FormRequest(
            self.url,
            callback=self.m_parse,
            method='GET',
            dont_filter=True,
        )
        return request

    def m_parse(self, response):
        pass
