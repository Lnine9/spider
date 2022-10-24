from urllib.parse import parse_qs

from scrapy import FormRequest

from BaseSpider.base_component.RequestResolver import RequestResolver
from BaseSpider.base_component.annoucement_request_resolver.ZGZF_Annoucement.ZGZF_Annouce_Req_Resolver import \
    ZGZF_START_TIME, ZGZF_END_TIME


class ZGZF_Agency_List_Page_Req_Resolver(RequestResolver):
    """
    允许自定义代码
    """

    def general_param(self) -> dict:
        # 必须在子方法中进行父方法调用
        super().general_param()

        # 以下为自定义代码
        gen_param = {}

        page_number = self.page_num
        url = 'http://jczy.ccgp.gov.cn/gs1/gs1agentreg/getPubList.regx'
        body = 'page={page}&rows=30&sort=regValidDate&order=desc'.format(page=page_number)
        call_back = self.req_attr.call_back,
        method = 'POST',

        gen_param['url'] = url
        gen_param['body'] = body
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
        result['start_time'] = ZGZF_START_TIME
        result['end_time'] = ZGZF_END_TIME

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
