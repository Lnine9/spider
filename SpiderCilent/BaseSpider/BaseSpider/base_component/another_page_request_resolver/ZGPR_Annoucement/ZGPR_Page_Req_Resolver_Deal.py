from urllib.parse import parse_qs, parse_qsl, urlencode

from scrapy import FormRequest

from BaseSpider.base_component.RequestResolver import RequestResolver


class ZGPR_Page_Req_Resolver_Deal(RequestResolver):
    """
    允许自定义代码
    """

    def general_param(self) -> dict:
        # 必须在子方法中进行父方法调用
        super().general_param()

        # 以下为自定义代码
        gen_param = {}

        page_number = self.page_num
        print("next_page:", page_number)
        url = "http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp"
        params = dict(parse_qsl(self.body))
        params['PAGENUMBER'] = page_number
        call_back = self.req_attr.call_back,
        method = 'POST',

        gen_param['url'] = url
        gen_param['body'] = urlencode(params)
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
