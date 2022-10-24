from scrapy import FormRequest

from BaseSpider.base_component.RequestResolver import RequestResolver


class YN_Annouce_Req_Resolver_ModifyBid(RequestResolver):

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
            method=self.method,
            formdata=self.body,
            dont_filter=self.dont_filter,
            meta=self.meta,
        )
        return request

    def m_parse(self, response):
        pass