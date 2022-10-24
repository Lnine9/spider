import datetime

from scrapy import FormRequest

# 初始网页请求
from BaseSpider.base_component.RequestResolver import RequestResolver

ZGZF_START_TIME = datetime.datetime.now().strftime('%Y')+':01:01'
ZGZF_END_TIME = datetime.datetime.now().strftime('%Y:%m:%d')

# 网站特定日期格式，冒号才能转换url日期后查询数量无误
# ZGZF_START_TIME = datetime.datetime.now().strftime('%Y')+":09:01"
# ZGZF_END_TIME = datetime.datetime.now().strftime('%Y:%m:%d')

# ZGZF_START_TIME ="2020:09:01"
# ZGZF_END_TIME = "2020:12:31"

class ZGZF_Annouce_Req_Resolver(RequestResolver):

    def general_param(self) -> dict:
        # 必须加载父类方法
        super().general_param()

        gen_param = {'url': self.url, 'call_back': self.call_back}
        return gen_param

    def create_request(self) -> FormRequest:
        # 必须加载父类方法
        super().create_request()
        if self.body:
            self.body['start_time'] = ZGZF_START_TIME
            self.body['end_time'] = ZGZF_END_TIME

        request = FormRequest(
            self.url,
            callback=self.m_parse,
            method=self.method,
            formdata=self.body,
            # dont_filter=self.dont_filter,
            dont_filter=True,
            meta=self.meta,
        )
        return request

    def m_parse(self, response):
        pass





