from urllib.parse import parse_qs, parse_qsl, urlencode

from scrapy import FormRequest

from BaseSpider.base_component.RequestResolver import RequestResolver

from .post_data import FORM_DATA, Stage

import logging


class GGZY_Page_Req_Resolver_CallBid_GCJS(RequestResolver):
    """
    允许自定义代码
    """

    def general_param(self) -> dict:
        # 必须在子方法中进行父方法调用
        super().general_param()

        # 以下为自定义代码
        gen_param = {}

        page_number = self.page_num
        url = "http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp"
        params = dict(parse_qsl(self.body))
        params['page_index'] = page_number
        call_back = self.req_attr.call_back
        method = 'POST'

        form_data = FORM_DATA
        form_data['PAGENUMBER'] = page_number
        form_data['DEAL_STAGE'] = Stage.CB_G.value
        # 工程建设
        form_data['DEAL_CLASSIFY'] = '01'

        gen_param['url'] = url
        gen_param['body'] = urlencode(form_data)
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
        form_data = parse_qs(self.body)

        logging.debug(form_data)

        request = FormRequest(
            self.url,
            callback=self.m_parse,
            method=self.method,
            formdata=form_data,
            dont_filter=self.dont_filter
        )
        return request

    def m_parse(self, response):
        pass
