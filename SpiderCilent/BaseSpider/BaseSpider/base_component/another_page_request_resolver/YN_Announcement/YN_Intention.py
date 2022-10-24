from urllib.parse import parse_qs, urlencode

from scrapy import FormRequest

from BaseSpider.base_component.RequestResolver import RequestResolver


class YN_Intention(RequestResolver):
    """
    允许自定义代码
    """

    def general_param(self) -> dict:
        # 必须在子方法中进行父方法调用
        super().general_param()
        # 以下为自定义代码
        gen_param = {}
        url = 'http://www.ccgp-yunnan.gov.cn/api/procurement/Procurement.purchaseList.svc?captchaCheckFlag=0&p=1'
        call_back = self.req_attr.call_back
        body = 'current={num}&rowCount=5&searchPhrase='.format(num=self.page_num)
        method = 'POST'

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
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "pragma": "no-cache",
            "x-requested-with": "XMLHttpRequest",
            "cookie": "__jsluid_h=692a63fe18d29360b67b8000e7fcb29b; "
                      "CoreSessionId=ea3ac91f2a15cd4847ed3c4d09b1582e953c1b785bc917bc; "
                      "_g_sign=dd04ac280bb9008ae1c76b96ffa54046; xincaigou=49737.2934.1035.0000; "
                      "route=d9b0266c2b8d5ad36e751f051b0faf07; "
                      "JSESSIONID=o84O61EVOe1StLfZSBUdZLjIdK-2DFCA9Rgi_AF8u6HOIesOHHws!1860972361",
            "Referer": "http://www.ccgp-yunnan.gov.cn/page/procurement/purchaseList.html",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62 "
        }

        request = FormRequest(
            self.url,
            callback=self.m_parse,
            method=self.method,
            headers=headers,
            body=self.body,
            dont_filter=self.dont_filter,
        )

        return request

    def m_parse(self, response):
        pass
