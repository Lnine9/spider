from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain


class SourceWebName(ParamObtain):
    @classmethod
    def get(cls):
        return '全国公共资源交易平台'

    @classmethod
    def check(cls, data: str):
        return True
