import json

from BaseSpider.tool.SpecialFormRequest import SpecialForm

from BaseSpider.base_component.RequestResolver import RequestResolver
from scrapy import FormRequest

class SCPR_Page_Req_Resolver_CallBid(RequestResolver):
    """翻页请求解析器"""

    """
    允许自定义代码
    """

    def general_param(self) -> dict:
        # 必须在子方法中进行父方法调用
        super().general_param()
        print(self.page_num[0])
        # 以下为自定义代码
        gen_param = {}
        url = 'http://ggzyjy.sc.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'
        body = {
            "token": "",
            "pn": int(int(self.page_num[0] - 1) * 12),
            "rn": 12,
            "sdt": "",
            "edt": "",
            "wd": "",
            "inc_wd": "",
            "exc_wd": "",
            "fields": "title",
            "cnum": "",
            "sort": "{'webdate':'0'}",
            "ssort": "title",
            "cl": 500,
            "terminal": "",
            "condition": [
                {
                    "fieldName": "categorynum",
                    "equal": "002001001",
                    "notEqual": None,
                    "equalList": None,
                    "notEqualList": None,
                    "isLike": True,
                    "likeType": 2
                }
            ],
            "time": [
                {
                    "fieldName": "webdate",
                    "startTime": "2020-1-9 00:00:00",
                    "endTime": "2020-1-12 23:59:59"
                }
            ],
            "highlights": "",
            "statistics": None,
            "unionCondition": None,
            "accuracy": "",
            "noParticiple": "0",
            "searchRange": None,
            "isBusiness": "1"
        }
        call_back = self.req_attr.call_back,
        method = 'POST',

        gen_param['url'] = url
        gen_param['body'] = json.dumps(body)
        gen_param['call_back'] = call_back
        gen_param['method'] = method

        return gen_param

    @property
    def create_request(self):
        # 必须在子方法中进行父方法调用
        page_num = "1"
        super().create_request()
        try:
            super().general_param()
            page_num = ''.join(list(self.page_num)[0][0])
        except:
            page_num = "1"

        '''
        以下为允许自定义方法

        '''

        if isinstance(self.url,tuple):
            self.url = self.general_param()["url"]

        request = SpecialForm(
            self.url,
            callback=self.m_parse,
            method=self.method,
            formdata={"special": self.body},
            dont_filter=self.dont_filter,
            special=True,
            meta={"currentPage": page_num}
        )

        return request

    def m_parse(self, response):
        pass
