from urllib.parse import parse_qs

from scrapy import FormRequest

from BaseSpider.base_component.RequestResolver import RequestResolver


class GZ_SJ_County_Modify_Page(RequestResolver):

    """
    允许自定义代码
    """
    def general_param(self) -> dict:
        # 必须在子方法中进行父方法调用
        super().general_param()

        # 以下为自定义代码
        gen_param = {}
        url = 'http://www.ccgp-guizhou.gov.cn/article-search.html',
        body = 'siteId=1&articlePageNo=' + str(self.req_attr.page_num) + '&category.id=1153454200156791&articlePageSize=15',
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







