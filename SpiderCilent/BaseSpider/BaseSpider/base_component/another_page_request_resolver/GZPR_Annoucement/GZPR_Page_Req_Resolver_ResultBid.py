from urllib.parse import parse_qs, urlencode

from scrapy import FormRequest

from BaseSpider.base_component.RequestResolver import RequestResolver


class GZPR_Page_Req_Resolver_ResultBid(RequestResolver):
    """
    允许自定义代码
    """

    def general_param(self) -> dict:
        # 必须在子方法中进行父方法调用
        super().general_param()

        # 以下为自定义代码
        gen_param = {}
        url = self.get_page_url()
        body = '',
        call_back = self.req_attr.call_back,
        method = 'GET',

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

    def get_page_url(self):
        page_number = self.page_num[0]
        base_url = 'http://ggzy.guizhou.gov.cn/igs/front/search/list.html'
        parameter = {
            'filter[DOCTITLE-like]': '',
            'filter[ChannelId]': '5377337,5377100,5376927',
            'filter[docSourceName]': '贵州省公共资源交易中心',
            'filter[inTypeName]': '2,交易结果公告',
            'filter[DocRelTime-gte]': '',
            'filter[DocRelTime-lte]': '',
            'filter[SITEID]': 500483,
            'pageNumber': page_number,
            'pageSize': 10,
            'index': 'index-bohoog',
            'type': 'zyzxjyxx_v8',
            'orderProperty': 'DocRelTime',
            'orderDirection': 'desc',
            'isPage': 'true'
        }
        data = urlencode(parameter)
        url = base_url + "?" + data
        return url
