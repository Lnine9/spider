from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain


class WebSite(ParamObtain):
    response = None

    @classmethod
    def set_data(cls, **kwargs):
        cls.response = kwargs['response']

    @classmethod
    def get(cls):
        return 'http://www.ggzy.gov.cn'

    @classmethod
    def check(cls, data: str):
        return True
