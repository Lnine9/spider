from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.base.param_obtain import \
    ParamObtain
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.tool import DealDate


class AncmTime(ParamObtain):

    @classmethod
    def set_data(cls, **kwargs):
        cls.response = kwargs['response']

    @classmethod
    def get(cls):
        response = SourceDatas.response
        time_str = response.xpath('//*[@class="p_o"]/*[contains(.,"发布时间")]//text()')[0]
        return DealDate.get_one_time_from_str(time_str)

    @classmethod
    def check(cls, data: str):
        return True
