from random import random
from urllib.parse import parse_qs

from scrapy import FormRequest

from ...RequestResolver import RequestResolver


class CQDX_W(RequestResolver):
    """
    允许自定义代码
    """

    def general_param(self) -> dict:
        # 必须在子方法中进行父方法调用
        super().general_param()

        # 以下为自定义代码
        gen_param = {}

        url = 'http://ztbzx.cqu.edu.cn/sfw_cms/e',
        body = 't_=' + str(random()) + '&window_=json&start=' + str(
            (self.page_num - 1) * 25 + 1) + '&limit=25&filter=&sort=beginTime%20desc&type=ZCGG&type=FBGG&type=BGGG&isEnd=&catalog=A&shopType=&notShopType=DYLY&categoryId=101720&keywords=&request_method_=ajax&browser_=notmsie&page=cms.psms.publish.query'
        call_back = self.req_attr.call_back,
        print(body)

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

        request = FormRequest(
            self.url,
            callback=self.m_parse,
            method=self.method,
            body=self.body,
            dont_filter=self.dont_filter,
            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': 'JSESSIONID=4B89B907BE8F4AA84135374D98E9609F; contextpath=%2Fsfw_cms',
                'Host': 'ztbzx.cqu.edu.cn',
                'Origin': 'http://ztbzx.cqu.edu.cn',
                'Pragma': 'no-cache',
                'Referer': 'http://ztbzx.cqu.edu.cn/sfw_cms/e?page=cms.psms.gglist&typeDetail=GS&shopping_type=DYLY',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
                'X-Requested-With': 'XMLHttpRequest'
            }
        )
        return request

    def m_parse(self, response):
        pass
